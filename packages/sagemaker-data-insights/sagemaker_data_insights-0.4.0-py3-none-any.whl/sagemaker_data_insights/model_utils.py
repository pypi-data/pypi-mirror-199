import copy
import logging
import numpy as np
import pandas as pd
from scipy import sparse as sp
from sagemaker_sklearn_extension.feature_extraction.date_time import DateTimeVectorizer
from sagemaker_sklearn_extension.feature_extraction.text import MultiColumnTfidfVectorizer
from sagemaker_sklearn_extension.preprocessing import NALabelEncoder, RobustLabelEncoder, RobustOrdinalEncoder
from sagemaker_sklearn_extension.impute import RobustImputer
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import IsolationForest
from sklearn.metrics import r2_score, roc_auc_score, accuracy_score, get_scorer, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold, KFold

from sagemaker_data_insights.const import TaskType as tt, QUICK_MODEL_METRICS, QUICK_MODEL_BASE_METRICS
from sagemaker_data_insights.const import FeatureType as ft
from sagemaker_data_insights.insights import Insights


def quick_model(  # noqa: C901
    x: pd.DataFrame,
    feature_types: dict,
    y: pd.Series,
    task: str,
    mode: str = "train validation split",
    metrics: list = None,
    xgb_args: dict = None,
    random_state: int = 0,
    n_jobs: int = 1,
    return_validation: bool = False,
):
    """
    Train a model on the data and report various prediction quality metrics. Three modes are supported:
        `train validation split`: Split the data into train and validation folds in ratio 80/20. The split is
            stratified for classification. Train an xgboost model on the training fold using early stopping on the
            validation fold. Calculate various prediction quality metrics on the train and validation folds
        `cross validation`: Split the data into k (k=5) equal folds. The split is stratified for classification. Repeat
            k times: train a model on k-1 folds with early stopping on the remaining fold. Concatenate the k train and
            validation folds and calculate various prediction quality metrics on the concatenated train and validation
            folds
            The returned model is a bagging (ensemble with weights 1/k) of the k models
        `auto`: use `cross validation` for datasets with less than 50k rows and `train validation split` for larger

    Parameters
    ----------
    x: pd.DataFrame,
        not encoded features
    feature_types: dict(str:str)
        - maps column names to column types
        - allowed types are all the types of `FeatureType`
        - only the columns of x that exists in `feature_types` will be used
    y : pd.Series
        Encoded and clean target column. For regression, all values must be finite floats (np.nan are not allowed).
        For classification, the labels must be encoded as numeric integers consecutive and starting from 0. For both
        regression and classification, it's recommended to use the label_encoder provided by `analyze_target_regression`
        or `analyze_target_classification` to encode the target column. Note that `analyze_target_regression` returns
        a list of invalid row indexes that must be removed from the data before calling `quick_model`
    task: str
        {tt.REGRESSION} or {tt.BINARY_CLASSIFICATION} or {tt.MULTICLASS_CLASSIFICATION}
    mode: str
        `train validation split` / `cross validation` / `auto` see description above
    metrics: list or None
        list of metrics to calculate. The metric strings are called as the parameter of `sklearn.metrics.get_scorer`.
        None will use the default set of metrics
    xgb_args : dict
        Parameters to pass to xgboost's constructor
    random_state : int
        random seed
    n_jobs : int
        number of cores for XGBoost and feature processing
    return_validation : bool
        if True then the fields 'y_validation' and 'pred_validation' will exist in the output

    Returns
    -------
    dict
        `quick_model_stats`: quick model metrics dictionary:
            1. "train" and "validation" for statistics for the training and validation folds. For each fold there are
            two keys "xgboost" and "trivial" for the results of the xgboost and trivial models. Each fold-model pair is
            a dictionary with all the metrics specified in `metrics`. When the task is classification there are also
            confusion_matrix and classification_report (produce by `sklearn.metrics.classification_report`). The
            confusion_matrix should be read using pandas.from_dict
            2. Additionally, the dictionary root contains the key 'insights' which is a list of insights (can be empty).
            The insights that can be thrown are: QUICK_MODEL_VERY_LOW and QUICK_MODEL_LOW
        `sample_size`: size of sample used to train the model, including both train and validation folds
        `mode`: mode used to produce the model. `train test split` or `cross validation`
        `xgboost_model`: trained xgboost model including data preprocessing steps. Should be used directly on the
            DataFrame as was the input to `quick_model`. For example: xgboost_model.preict(data_frame.astype(str))
        `y_validation` : (np.array) The validation fold of the target column data provided in the input as `y`. Returned
            only when return_validation is True
        `pred_validation` : (np.array) The out-of-sample prediction values for the validation fold. Prediction is
            returned for regression and class probabilities for classification. Returned only when return_validation is
            True
"""
    assert task in [tt.REGRESSION, tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION]
    sample_size = x.shape[0]
    if mode == "auto":
        mode = "cross validation" if sample_size < 50000 else "train validation split"
    assert mode in ["train validation split", "cross validation"]
    if metrics is None:
        metrics = QUICK_MODEL_METRICS[task]
    logging.info(
        "Quick model: task: %s, number of rows: %d, number of features: %d, mode: %s",
        task,
        sample_size,
        len(feature_types),
        mode,
    )
    logging.debug("Quick model: encoding features")
    encoded_features_dict = _encode_features(feature_types, x, None, True, n_jobs=n_jobs)

    # XGBoost base configuration
    xgb_args_base = {
        "n_estimators": 1000,
        "learning_rate": 0.025,
        "random_state": random_state,
        "use_label_encoder": False,
        "n_jobs": n_jobs,
    }
    if task == tt.BINARY_CLASSIFICATION:
        xgb_args_base["eval_metric"] = "logloss"
    elif task == tt.MULTICLASS_CLASSIFICATION:
        xgb_args_base["eval_metric"] = "mlogloss"

    # Override xgboost args if provided
    if xgb_args:
        xgb_args_base.update(xgb_args)
    xgb_args = xgb_args_base

    # Store out of sample and training y and predictions. Will be used to calculate metrics
    out_of_sample = {"y": [], "xgboost": [], "trivial": []}
    train = {"y": [], "xgboost": [], "trivial": []}

    if mode == "train validation split":
        logging.debug("Quick model: training (train test split)")
        x_train, x_validation, y_train, y_validation = _safe_train_test_split(
            encoded_features_dict["transformed_data"],
            y.to_numpy(),
            test_size=0.2,
            stratify=(None if task == tt.REGRESSION else y),
            random_state=random_state,
        )
        xgb_model, trivial_model = _fit_models((x_train, y_train), (x_validation, y_validation), task, xgb_args)
        _append_to_dict(out_of_sample, x_validation, y_validation, xgb_model, trivial_model, task)
        _append_to_dict(train, x_train, y_train, xgb_model, trivial_model, task)
    else:
        # Cross validation
        logging.debug("Quick model: training (cross validation)")
        num_classes = len(np.unique(y))
        n_splits = 5
        folds = (
            KFold(n_splits=n_splits).split(encoded_features_dict["transformed_data"])
            if task == tt.REGRESSION
            else StratifiedKFold(n_splits=n_splits).split(encoded_features_dict["transformed_data"], y)
        )
        xgb_models = []
        for fold_idx, (train_index, validation_index) in enumerate(folds):
            logging.debug(f"Quick model: training fold {fold_idx}")
            x_train = encoded_features_dict["transformed_data"][train_index]
            y_train = y.to_numpy()[train_index].reshape((-1, 1))
            if task != tt.REGRESSION:
                # Make sure that y_train includes all the classes by adding rows where all features are NaNs. This
                # doesn't affect the trained model. It's a workaround as XGBoost does not support specifying all
                # possible target values
                x_train = (np.vstack if sp.sputils.isdense(x_train) else sp.vstack)(
                    [x_train, np.full((num_classes, x_train.shape[1]), np.nan)]
                )
                y_train = np.vstack([y_train, np.arange(num_classes).reshape((-1, 1))])
            x_validation = encoded_features_dict["transformed_data"][validation_index]
            y_validation = y.to_numpy()[validation_index]
            xgb_model, trivial_model = _fit_models((x_train, y_train), (x_validation, y_validation), task, xgb_args)
            _append_to_dict(out_of_sample, x_validation, y_validation, xgb_model, trivial_model, task)
            _append_to_dict(train, x_train, y_train, xgb_model, trivial_model, task)
            xgb_models.append(xgb_model)
        xgb_model = (EnsembleRegressor if task == tt.REGRESSION else EnsembleClassifier)(xgb_models)

    for d in [out_of_sample, train]:
        for k in ["y", "xgboost", "trivial"]:
            d[k] = np.vstack(d[k])

    logging.debug("Quick model: calculating metrics")

    quick_model_stats = {}
    for data_type, preds in [("train", train), ("validation", out_of_sample)]:
        quick_model_stats[data_type] = {}
        for model_name in ["xgboost", "trivial"]:
            quick_model_stats[data_type][model_name] = {}
            quick_model_stats[data_type][model_name] = _calculate_metrics(
                DummyPredictor(task), preds[model_name], preds["y"], metrics
            )

        if task in [tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION]:
            quick_model_stats[data_type]["xgboost"]["classification_report"] = classification_report(
                preds["y"], DummyPredictor(task).predict(preds["xgboost"]), output_dict=True
            )
            cm = confusion_matrix(preds["y"], DummyPredictor(task).predict(preds["xgboost"]))
            cm = pd.DataFrame(
                data=cm,
                columns=[f"predicted label {idx}" for idx in range(cm.shape[0])],
                index=[f"true label {idx}" for idx in range(cm.shape[0])],
            )
            quick_model_stats[data_type]["xgboost"]["confusion_matrix"] = cm.to_dict()

    quick_model_stats["insights"] = _quick_model_insights(task, quick_model_stats["validation"])
    d = {
        "quick_model_stats": quick_model_stats,
        "sample_size": sample_size,
        "mode": mode,
        "xgboost_model": Pipeline([("preprocessing", encoded_features_dict["pipeline"]), ("model", xgb_model)]),
    }
    if return_validation:
        d["pred_validation"] = out_of_sample["xgboost"]
        d["y_validation"] = out_of_sample["y"]
    return d


def _append_to_dict(d: dict, x, y, xgb_model, trivial_model, task: str):
    # Helper function to append predictions and y to dictionary
    d["y"].append(y.reshape((-1, 1)))
    d["xgboost"].append(xgb_model.predict(x).reshape((-1, 1)) if task == tt.REGRESSION else xgb_model.predict_proba(x))
    d["trivial"].append(
        trivial_model.predict(x).reshape((-1, 1)) if task == tt.REGRESSION else trivial_model.predict_proba(x)
    )


def _fit_models(train_fold: tuple, validation_fold: tuple, task: str, xgb_args: dict):
    """
    Fit XGBoost model and trivial model.
    Trivial model is mean for regression and most frequent class for classification

    Parameters
    ----------
    train_fold: a tuple of array like objects (x_train, y_train)
    validation_fold: a tuple of array like objects (x_validation, y_validation)
    task: a string from sagemaker_data_insights.const.TaskType
    xgb_args: a dictionary of parameters for XGBoost

    Returns
    -------
    Two fitted models: XGBoost and trivial
    """
    from sagemaker_data_insights.xgboost_utils import XGBRegressorWrapper, XGBClassifierWrapper
    xgb_model = XGBRegressorWrapper(**xgb_args) if task == tt.REGRESSION else XGBClassifierWrapper(**xgb_args)
    xgb_model.fit(
        X=train_fold[0],
        y=train_fold[1],
        early_stopping_rounds=10,
        eval_set=[(validation_fold[0], validation_fold[1])],
        verbose=False,
    )
    logging.debug("Quick model: training trivial model")
    trivial_model = (
        DummyRegressor(strategy="mean") if task == tt.REGRESSION else DummyClassifier(strategy="most_frequent")
    )
    trivial_model.fit(X=train_fold[0], y=train_fold[1])
    return xgb_model, trivial_model


def anomaly_detection(x: pd.DataFrame, feature_types: dict, y: pd.Series, random_state: int = 0, n_jobs: int = 1):
    """
    Anomalous samples are detected using the Isolation forest algorithm that analyzes the data after a basic
    preprocessing was performed. The Isolation forest algorithm associates an anomaly score to each
    sample (row) of the dataset. Low anomaly scores imply anomalous samples and high scores are associated with
    non-anomalous samples. Samples with negative anomaly score are usually considered anomalous and samples with
    positive anomaly score are considered non-anomalous.

    Parameters
    ----------
    x: pd.DataFrame,
        not encoded features
    feature_types: dict(str:str)
        - maps column names to column types
        - allowed types are all the types of `FeatureType`
        - only the columns of x that exists in `feature_types` will be used
    y : pd.Series or None
        Encoded and clean target column. For regression, all values must be finite floats (np.nan are not allowed).
        For classification, the labels must be encoded as numeric integers consecutive and starting from 0. For both
        regression and classification, it's recommended to use the label_encoder provided by `analyze_target_regression`
        or `analyze_target_classification` to encode the target column. Note that `analyze_target_regression` returns
        a list of invalid row indexes that must be removed from the data before calling `quick_model`
    random_state : int
        random seed
    n_jobs : int
        number of cores to use

    Returns
    -------
    dict
        "anomaly_scores": list of isolation forest scores for each sample
        "sample_size": size of sample used for anomaly detection
"""
    logging.info("Anomaly detection: number of rows: %d, number of features: %d", x.shape[0], len(feature_types))
    encoded_features_dict = _encode_features(feature_types, x, None, False, n_jobs=n_jobs)
    x_encoded = encoded_features_dict["transformed_data"]

    # for datetime features that might return np.nan
    if sp.issparse(x_encoded):
        x_encoded.data[~np.isfinite(x_encoded.data)] = 0.0
        if y is not None:
            sp.hstack([x_encoded, y.to_numpy().reshape((-1, 1))])
    else:
        x_encoded = x_encoded.astype(np.float32)
        x_encoded[~np.isfinite(x_encoded)] = 0
        if y is not None:
            x_encoded = np.hstack([x_encoded, y.to_numpy().reshape((-1, 1))])

    logging.info("Anomaly detection: training IsolationForest")
    anomaly_scores = (
        IsolationForest(random_state=random_state, n_jobs=n_jobs).fit(x_encoded).decision_function(x_encoded)
    )
    return {"anomaly_scores": list(anomaly_scores), "sample_size": len(x)}


def duplicate_rows(x: pd.DataFrame, y: pd.Series, max_num_duplicates: int = 10):
    """
    Identify duplicate rows using `pandas.duplicated`

    Parameters
    ----------
    x: pd.DataFrame,
        not encoded features
    y : pd.Series or None
        target column, could be either encoded or not
    max_num_duplicates: int
        the maximum number of duplicate rows to return in the duplicate_rows data frame

    Returns
    -------
    dict
        "duplicate_rows": pd.DataFrame of the most {max_num_duplicates} common duplicate rows. The data frame was
            converted to dictionary using pd.to_dict() and need to be converted back
        "sample_size": size of sample used for duplicate rows detection
        "duplicate_ratio": the ratio between the number of duplicate rows to the number of rows in the input dataframe
        "insights": list of insights, can include the insights MANY_DUPLICATE_ROWS and DUPLICATE_ROWS
"""
    if y is not None:
        assert y.name not in list(x.columns)
        x = x.copy()
        x[y.name] = y
    duplicate_rows_list = x.duplicated(keep=False)
    duplicate_ratio = sum(duplicate_rows_list) / len(x)
    duplicate_count_key = "Duplicate count"
    duplicated_rows = (
        x[duplicate_rows_list].groupby(list(x.columns), dropna=False).size().reset_index(name=duplicate_count_key)
    )
    # Reorder the columns of duplicated_rows so {duplicate_count_key} will be the first column
    tmp_columns = list(duplicated_rows.columns)
    tmp_columns.remove(duplicate_count_key)
    duplicated_rows = (
        duplicated_rows[[duplicate_count_key] + tmp_columns]
        .sort_values(duplicate_count_key, ascending=False)
        .reset_index(drop=True)
        .head(max_num_duplicates)
    )
    insights = []
    if duplicate_ratio > Insights.MANY_DUPLICATE_ROWS_THRESHOLD:
        insights.append(
            Insights.generate(
                Insights.MANY_DUPLICATE_ROWS, Insights.HIGH, {"sample_size": len(x), "duplicate_ratio": duplicate_ratio}
            )
        )
    elif duplicate_ratio > 0:
        insights.append(
            Insights.generate(
                Insights.DUPLICATE_ROWS, Insights.MEDIUM, {"sample_size": len(x), "duplicate_ratio": duplicate_ratio}
            )
        )
    return {
        "duplicate_rows": duplicated_rows.to_dict(),
        "duplicate_ratio": duplicate_ratio,
        "sample_size": len(x),
        "insights": insights,
    }


def _safe_train_test_split(x, y, test_size, stratify=None, random_state: int = 0):
    """
    A safe version of sklearn.model_selection.train_test_split that can handle classes with a single instance when
    applying stratified splitting. This is done by adding all the observations with a single instance label to the
    training fold.
    """
    if stratify is None:
        return train_test_split(x, y, test_size=test_size, stratify=stratify, random_state=random_state)
    values, index, counts = np.unique(stratify, return_index=True, return_counts=True)
    valid = np.full(x.shape[0], True)
    for i in range(len(values)):
        if counts[i] == 1:
            valid[index[i]] = False

    if np.sum(valid) == 0:
        logging.warning("For every class in target, only one label is available.")
        return train_test_split(x, y, test_size=test_size, stratify=None, random_state=random_state)
    elif sum(valid) < stratify.shape[0]:
        X_train, X_validation, y_train, y_validation = train_test_split(
            x[valid], y[valid], test_size=test_size, stratify=stratify[valid], random_state=random_state
        )
        stack_f = sp.vstack if sp.issparse(X_train) else np.vstack
        X_train = stack_f([X_train, x[~valid]])
        y_train = np.concatenate([y_train, y[~valid]], axis=0)
        return X_train, X_validation, y_train, y_validation
    else:
        return train_test_split(x, y, test_size=test_size, stratify=stratify, random_state=random_state)


def _quick_model_insights(task, validation_metrics):
    base_metric = QUICK_MODEL_BASE_METRICS[task]
    insights = []
    if base_metric in validation_metrics["xgboost"] and base_metric in validation_metrics["trivial"]:
        if validation_metrics["xgboost"][base_metric] < validation_metrics["trivial"][base_metric]:
            insights.append(Insights.generate(Insights.QUICK_MODEL_VERY_LOW, Insights.HIGH))
        elif (
            validation_metrics["xgboost"][base_metric]
            < Insights.QUICK_MODEL_LOW_BIAS
            + (1 - Insights.QUICK_MODEL_LOW_BIAS) * validation_metrics["trivial"][base_metric]
        ):
            insights.append(Insights.generate(Insights.QUICK_MODEL_LOW, Insights.MEDIUM))
    else:
        logging.warning("Base_metric %s was not found in quick model metrics", base_metric)
    return insights


def _calculate_metrics(model, x, y, metrics):
    ret = {}
    for m in metrics:
        try:
            ret[m] = get_scorer(m)(model, x, y.ravel())
        except ValueError as e:
            logging.error(e)
            ret[m] = np.nan
    return ret


def _get_label_encoder(task: str, y: np.array):
    """Prepares `LabelEncoder` against labels specified in an array, and returns a fitted `LabelEncoder` transform.

    For regression, we change any non-numeric value to nan. For multiclass and binary classification, we encode them.

    Args:
        task (str): The problem type. Must be a constant from [REGRESSION, BINARY_CLASSIFICATION,
        MULTICLASS_CLASSIFICATION].
        y (np.array): target data to use for fitting.

    Returns:
        function: `LabelEncoder` transform after fitting.
    """
    if task == tt.REGRESSION:
        return NALabelEncoder().fit(y)

    if task == tt.BINARY_CLASSIFICATION:
        # This code is to insure that the minority class is encoded as `1`
        y_transformed = LabelEncoder().fit_transform(y)
        y_valid = y[np.isfinite(y_transformed)]
        labels, counts = np.unique(y_valid, return_counts=True)
        labels_count = []
        for idx, label in enumerate(labels):
            labels_count.append((label, counts[idx]))
        if labels_count[0][1] > labels_count[1][1]:
            majority_label = labels_count[0][0]
            minority_label = labels_count[1][0]
        else:
            majority_label = labels_count[1][0]
            minority_label = labels_count[0][0]
        return RobustLabelEncoder(
            labels=[majority_label], fill_label_value=minority_label, include_unseen_class=True
        ).fit(y)

    return RobustLabelEncoder().fit(y)


def _get_feature_transform(feature_type: str, unknown_as_nan: bool):
    """
    Returns the default feature transform used by data_insights to do various tasks that require feature encoding
    including: quick model, anomaly detection, prediction power and more.
"""
    from sagemaker_sklearn_extension.feature_extraction.sequences import TSFeatureExtractor

    # TODO: temporially removing TSFeatureExtractor for Ganymede
    return {
        ft.NUMERIC: RobustImputer(strategy="constant", fill_values=np.nan) if unknown_as_nan else RobustImputer(),
        ft.CATEGORICAL: RobustOrdinalEncoder(unknown_as_nan=unknown_as_nan),
        ft.BINARY: RobustOrdinalEncoder(unknown_as_nan=unknown_as_nan),
        ft.TEXT: MultiColumnTfidfVectorizer(max_features=100),
        ft.DATETIME: DateTimeVectorizer(mode="ordinal"),
        ft.VECTOR: TSFeatureExtractor(extraction_type="minimal"),
    }[feature_type]


def _encode_features(
    feature_types: dict, data: pd.DataFrame, allowed_types: list, unknown_as_nan: bool, n_jobs: int = 1
):
    """
    Encodes the feature column vectors based on the provided feature type. {NUMERIC}, {BINARY}, {TEXT}, {DATETIME},
    {VECTOR} and {CATEGORICAL} feature types are supported. If feature vector of any other allowed type is passed,
    the feature data will not be encoded.

    Parameters
    ----------
     feature_types: dict
        Maps the columns names / feature names in [data] its the type (str)

    data: pandas.DataFrame
        Feature vectors

    allowed_types: list or None
        A list of allowed features types. An error is raised if a feature type is not in the list.
        When None all types are allowed

    unknown_as_nan: bool
        Whether to encode invalid/unknown values as np.nan or impute them

    n_jobs : int
        number of cores to use

    Raises
    ----------
    TypeError
        Error is raised if the given feature type is not in [allowed_types] or not supported.
        Error is also raised if feature data does not match feature type.
        (Eg: Binary feature column has more than two categories)

    Returns
    ----------
    dict:
        'transformed_data': (np.array) Encoded feature data
            The order of the features in the input data (in `feature_types`) is maintained in the encoded data.
        'pipeline': the trained pipeline used for feature preprocessing
    """

    if feature_types == {}:
        logging.warning("feature_types empty")
        return {"transformed_data": np.empty(data.shape), "pipeline": Pipeline}

    # Workaround for TFIDF failing when the length of all strings is less than 2 - use the transform for categorical
    # features
    feature_types = copy.deepcopy(feature_types)
    for feature_name, feature_type in feature_types.items():
        if feature_type == ft.TEXT:
            max_length = data[feature_name].astype(str).map(lambda x: len(x)).max()
            if max_length < 2:
                feature_types[feature_name] = ft.CATEGORICAL

    # Creating the transform list
    transformers = []
    for idx, (feature_name, feature_type) in enumerate(feature_types.items()):
        if allowed_types and feature_type not in allowed_types:
            # Raise error if feature type is not in allowed_types list
            raise TypeError("Feature Type " + feature_type + " is not permitted")
        transformers.append((f"transform{idx}", _get_feature_transform(feature_type, unknown_as_nan), [feature_name]))
    pipeline = ColumnTransformer(transformers, n_jobs=n_jobs).fit(data.astype(str))
    return {"transformed_data": pipeline.transform(data.astype(str)), "pipeline": pipeline}


def _calc_prediction_power(
    x: np.ndarray,
    y: np.ndarray,
    task: str,
    random_state: int = 0,
    min_samples: int = 100,
    n_estimators: int = 50,
    n_jobs: int = 1,
):
    """
    Derive the prediction power of a feature using univariate predictor. We train an XGBoost model on the single feature
    and use the loss as measure of prediction power. This score is normalized by comparing it to the loss of the trivial
    model.

    Parameters
    ----------
    x : np.ndarray
        encoded feature data. A matrix numpy array of size (height, num_features). All values must be floats or np.nan
    y : np.ndarray
        Encoded and clean target column. For regression, all values must be finite floats (np.nan are not allowed).
        For classification, the labels must be encoded as numeric integers consecutive and starting from 0. For both
        regression and classification, it's recommended to use the label_encoder provided by `analyze_target_regression`
        or `analyze_target_classification` to encode the target column. Note that `analyze_target_regression` returns
        a list of invalid row indexes that must be removed from the data before calling `_baseline_prediction_power`
    task : str in [REGRESSION, BINARY_CLASSIFICATION, MULTICLASS_CLASSIFICATION]
    random_state: int
        integer to use as random seed
    min_samples : int
        if the data comprises less than {min_samples} then we don't have enough samples to calculate prediction power
        and the function will return np.nan
    n_estimators : int
        Number of XGBoost iterations
    n_jobs : int
        number of cores for XGBoost
"""
    from sagemaker_data_insights.xgboost_utils import XGBRegressorWrapper, XGBClassifierWrapper
    if x.shape[0] < min_samples:
        logging.warning(
            f"The number of samples in x for _calc_prediction_power is {x.shape[0]} which is smaller than "
            f"the minimum required of {min_samples}."
        )
        return np.nan, np.nan
    XGBargs = {"n_estimators": n_estimators, "use_label_encoder": False, "n_jobs": n_jobs}
    if task == tt.BINARY_CLASSIFICATION:
        XGBargs["eval_metric"] = "logloss"
    elif task == tt.MULTICLASS_CLASSIFICATION:
        XGBargs["eval_metric"] = "mlogloss"
    model = XGBRegressorWrapper(**XGBargs) if task == tt.REGRESSION else XGBClassifierWrapper(**XGBargs)
    X_train, X_validation, y_train, y_validation = _safe_train_test_split(
        x, y, test_size=0.2, stratify=(None if task == tt.REGRESSION else y), random_state=random_state
    )
    if len(np.unique(y_validation)) == 1:
        logging.error("The number of unique items in the encoded target column validation set is 1")
        return np.nan, np.nan
    try:
        model.fit(
            X=X_train, y=y_train, early_stopping_rounds=10, eval_set=[(X_validation, y_validation)], verbose=False
        )
    except Exception as ex:
        logging.error(ex)
        return np.nan, np.nan
    score = _model_score(X_validation, y_validation, model, task)
    baseline_score = _baseline_prediction_power(y_validation, task)
    norm_score = max((score - baseline_score) / (1 - baseline_score), 0)
    return float(score), float(norm_score)


def _model_score(x: np.ndarray, y: np.ndarray, model, task: str):
    if task == tt.REGRESSION:
        return r2_score(y, model.predict(x))
    elif task == tt.BINARY_CLASSIFICATION:
        return roc_auc_score(y, model.predict_proba(x)[:, 1])
    elif task == tt.MULTICLASS_CLASSIFICATION:
        return accuracy_score(y, model.predict(x))
    raise ValueError(
        f"task {task} is not allowed. Allowed types are {tt.REGRESSION}, {tt.BINARY_CLASSIFICATION} and "
        f"{tt.MULTICLASS_CLASSIFICATION}"
    )

def _calc_correlation(
    x: np.ndarray,
    y: np.ndarray
):
    return float(pd.DataFrame(x).corrwith(pd.DataFrame(y)))


class DummyPredictor:
    # A dummy predictor that returns the input as prediction. It is used to enable using sklearn scorers which require
    # a model supporting predict() and predict_proba()
    def __init__(self, task):
        self.task = task

    def fit(self, task):
        raise Exception("fit for DummyPredictor should not be called")

    def predict(self, X):
        if self.task == tt.REGRESSION:
            return X
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)

    def predict_proba(self, proba):
        assert self.task != tt.REGRESSION
        return proba


class EnsemblePredictor:
    # Parent class for EnsembleRegressor and EnsembleClassifier
    def __init__(self, models, weights=None):
        self.models = models
        self.weights = weights if weights else [1 / len(models) for _ in models]
        assert np.sum(self.weights) == 1

    def fit(self, X, y):
        raise Exception("Fit for shouldn't be called for ensemble predictor")


class EnsembleRegressor(EnsemblePredictor):
    # Ensamble of pretrained models for regression
    def __init__(self, *args, **kwargs):
        super(EnsembleRegressor, self).__init__(*args, **kwargs)

    def calc_models(self, X):
        preds = [m.predict(X) * self.weights[idx] for idx, m in enumerate(self.models)]
        return np.nansum(np.stack(preds), axis=0)

    def predict(self, X):
        return self.calc_models(X)


class EnsembleClassifier(EnsemblePredictor):
    # Ensamble of pretrained models for classification
    def __init__(self, *args, **kwargs):
        super(EnsembleClassifier, self).__init__(*args, **kwargs)

    def calc_models(self, X):
        preds = [m.predict_proba(X) * self.weights[idx] for idx, m in enumerate(self.models)]
        return np.nansum(np.stack(preds), axis=0)

    def predict(self, X):
        return np.argmax(self.calc_models(X), axis=1)

    def predict_proba(self, X):
        return self.calc_models(X)


def _baseline_prediction_power(y: np.ndarray, task):
    """
    Derive the baseline prediction power. This is the prediction of a trivial model:
        REGRESSION: r2 of the trivial model that always predicts the labels average is 0
        BINARY_CLASSIFICATION: AUC of any constant predictor is 0.5
        MULTICLASS_CLASSIFICATION: the accuracy of the trivial model that always predicts the most common label is
        given by the ratio between the frequency of the most common label to the number of elements in y

    Parameters
    ----------
    y : np.ndarray
        Encoded and clean target column. For regression, all values must be finite floats (np.nan are not allowed).
        For classification, the labels must be encoded as numeric integers consecutive and starting from 0. For both
        regression and classification, it's recommended to use the label_encoder provided by `analyze_target_regression`
        or `analyze_target_classification` to encode the target column. Note that `analyze_target_regression` returns
        a list of invalid row indexes that must be removed from the data before calling `_baseline_prediction_power`
    task : str in [REGRESSION, BINARY_CLASSIFICATION, MULTICLASS_CLASSIFICATION]
"""
    assert task in [tt.REGRESSION, tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION]
    return float(
        {
            tt.REGRESSION: 0,
            tt.BINARY_CLASSIFICATION: 0.5,
            tt.MULTICLASS_CLASSIFICATION: max(np.unique(y, return_counts=True)[1]) / y.shape[0],
        }[task]
    )
