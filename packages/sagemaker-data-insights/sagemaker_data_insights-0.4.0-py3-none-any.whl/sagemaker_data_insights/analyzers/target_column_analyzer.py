import logging
import scipy
import pandas as pd
import numpy as np

from sagemaker_data_insights.const import INSIGHTS, TaskType as tt
from sagemaker_data_insights.analyzers.insights.utils import get_label_encoder
from sagemaker_data_insights.analyzers.insights.model_insights import regression_insights, classification_insights
from sagemaker_data_insights.utils.column_utils import unique_without_whitespaces
from sagemaker_data_insights.histogram_functions import calc_robust_histogram, robust_histogram_num_outliers


def analyze_target_regression(
        y: pd.Series, metrics: dict, num_bins: int = 20, max_num_common_labels: int = 10, max_num_outliers: int = 5,
        get_histogram: bool = False
):
    """
    Target column analyzer for regression task

    Parameters
    ----------
    y : pandas.Series
        target column (could be raw. Doesn't have to be encoded)
    metrics : dict
         dictionary that must include all the keys in REQUIRED_TARGET_METRICS. While `analyze_target_regression`
         is usually applied on a sample of the data, the metrics should be calculated on the whole data or on a larger
         sample
    num_bins : int >= 3
        number of bins in histograms
    max_num_common_labels : int >= 1
        max number of most common labels to return in `labels` and `label_counts` fields
    max_num_outliers : int >= 0
        max number of outliers to to return in `low_outlier_idxs` and `high_outlier_idxs` fields
    get_histogram: bool, False
        whether to produce histogram and robust histogram, default to False

    Returns
    -------
    dict: data insights metrics
        labels: list of all labels in the target column sorted by descending count order
        label_counts: list of label counts sorted by descending count order
        valid_ratio: ratio of the number of numeric finite values to the number of samples
        name: name of target column
        outliers_ratio: ratio between number of outliers to number of samples
        mean: mean of numeric values (outliers included)
        median: median of numeric values (outliers included)
        skew: skew of numeric values (outliers included). Calculated using scipy.stats.skew
        kurtosis: kurtosis of numeric values (outliers included). Calculated using scipy.stats.kurtosis
        histogram: histogram of numeric values (outliers included). Calculated using numpy.histogram
        robust_histogram: robust_histogram of numeric values (outliers included). Calculated using calc_robust_histogram
        metrics: metrics provided in input
        {cs.INSIGHTS}: a list of insights. Can include the following insights: SKEWED_TARGET, HEAVY_TAILED_TARGET,
            TARGET_OUTLIERS, REGRESSION_FREQUENT_LABEL, REGRESSION_NONNUMERIC and REGRESSION_MANY_NONNUMERIC. The
            insights are documented in `insights.py`
    dict: auxiliary dict including the following:
        label_encoder: `LabelEncoder` transform
        valid_row_idxs: (np.ndarray) valid rows indicator
        low_outlier_idxs: (list) indexes of low value outliers for regression
        high_outlier_idxs: (list) indexes of high value outliers for regression
"""
    profiles = {}

    label_encoder, labels, label_counts, y_encoded, _ = _analyze_target(y, tt.REGRESSION, metrics)
    valid_rows = np.isfinite(y_encoded).ravel()
    valid_encoded = y_encoded[valid_rows]
    valid_row_idxs = np.nonzero(valid_rows)[0]

    aux = {"label_encoder": label_encoder}

    if get_histogram:
        count, bin_edges = np.histogram(valid_encoded, bins=num_bins)
        histogram = {
            "hist_count": count.astype(int).tolist(),
            "hist_edges": bin_edges.astype(float).tolist(),
            "lower_bin_is_outlier": False,
            "upper_bin_is_outlier": False,
        }
        profiles.update({"histogram": histogram})
    robust_histogram = calc_robust_histogram(valid_encoded, num_bins=num_bins)
    # count outliers to calculate `outliers_ratio`
    num_outliers = robust_histogram_num_outliers(robust_histogram)

    # get idxs of lowest outliers to be output as `low_outlier_idxs`
    low_outlier_idxs = []
    if robust_histogram["lower_bin_is_outlier"]:
        for idx in np.argsort(valid_encoded.ravel())[:max_num_outliers]:
            value = valid_encoded[idx]
            if value < robust_histogram["hist_edges"][1]:
                low_outlier_idxs.append(valid_row_idxs[idx])
    # get idxs of highest outliers to be output as `high_outlier_idxs`
    high_outlier_idxs = []
    if robust_histogram["upper_bin_is_outlier"]:
        for idx in reversed(np.argsort(valid_encoded.ravel())[-max_num_outliers:]):
            value = valid_encoded[idx]
            if value > robust_histogram["hist_edges"][-2]:
                high_outlier_idxs.append(valid_row_idxs[idx])

    aux.update({"invalid_row_idxs": np.nonzero(~valid_rows)[0], "low_outlier_idxs": low_outlier_idxs,
                "high_outlier_idxs": high_outlier_idxs})

    outliers_ratio = float(num_outliers / valid_encoded.shape[0])
    skew = float(scipy.stats.skew(valid_encoded.ravel()))
    kurtosis = float(scipy.stats.kurtosis(valid_encoded.ravel()))

    # Check for target insights
    insights = regression_insights(outliers_ratio, skew, kurtosis, labels, label_counts, metrics)

    profiles.update({
        "labels": labels[:max_num_common_labels],
        "label_counts": label_counts[:max_num_common_labels],
        "valid_ratio": float(metrics["numeric_finite_count"] / metrics["nrows"]),
        "missing_ratio": float(
            (metrics["null_like_count"] + metrics["empty_count"] + metrics["whitespace_count"]) / metrics["nrows"]
        ),
        "name": y.name,
        "outliers_ratio": outliers_ratio,
        "mean": float(np.nanmean(valid_encoded)),
        "median": float(np.nanmedian(valid_encoded)),
        "skew": skew,
        "kurtosis": kurtosis,
        INSIGHTS: insights,
        "metrics": metrics,
        "robust_histogram": robust_histogram,
    })

    return (
        profiles,
        aux
    )


def analyze_target_classification(
    y: pd.Series, metrics: dict, max_num_common_labels: int = 10,
):
    """
    Target column analyzer for classification task

    Parameters
    ----------
    y : pandas.Series
        target column (not encoded)
    metrics : dictionary that must include all the keys in REQUIRED_TARGET_METRICS.
        While `analyze_target_classification` is usually applied on a sample of the data,
        the metrics should be calculated on the whole data or on a larger sample. See const.py
    max_num_common_labels : int >= 1
        max number of most common labels to return in `labels` and `label_counts` fields

    Returns
    -------
    dict: data insights metrics
        labels: list of all labels in the target column sorted by descending count order
        label_counts: list of label counts sorted by descending count order
        valid_ratio: ratio of the number of not null like values to the number of samples
        name: name of target column
        frequent_elements: calculated based on `labels` and `label_counts` provided in metrics
        metrics: metrics provided in input
        insights: a list of insights. Can include the following insights: VERY_SMALL_MINORITY, HIGH_TARGET_CARDINALITY,
        RARE_TARGET_LABEL and SKEWED_LABEL_FREQUENCY. The insights are documented in `insights.py`
    dict: auxiliary dict including the following:
        label_encoder: `LabelEncoder` transform
        valid_row_idxs: (np.ndarray) valid rows indicator
        y_map: dict. label_encoder mapping e.g. {0: 'dog', 1: 'cat', 2: 'mouse'}
        task: str either BINARY_CLASSIFICATION or MULTICLASS_CLASSIFICATION
"""
    try:
        # When the data type of y is string: Null, empty and cells of only whitespace are considered missing
        valid_rows = (~pd.isnull(y)) & (y.str.strip() != "")
    except AttributeError:
        # When the data type of y is not string: only Nulls are considered missing
        valid_rows = ~pd.isnull(y)
    y = y[valid_rows]

    task = tt.BINARY_CLASSIFICATION if len(np.unique(y.to_numpy().astype(str))) == 2 else tt.MULTICLASS_CLASSIFICATION
    logging.debug("task = %s", task)
    label_encoder, labels, label_counts, _, sample_size = _analyze_target(y, task, metrics)
    y_map = {label_encoder.transform([label])[0]: label for label in labels}

    # Check for target insights
    insights = classification_insights(task, labels, label_counts, sample_size)
    sum_label_counts = np.sum(label_counts)

    return (
        {
            "labels": labels[:max_num_common_labels],
            "label_counts": label_counts[:max_num_common_labels],
            "missing_ratio": float(
                (metrics["null_like_count"] + metrics["empty_count"] + metrics["whitespace_count"]) / metrics["nrows"]
            ),
            "valid_ratio": float(
                (metrics["nrows"] - metrics["null_like_count"] - metrics["empty_count"] - metrics["whitespace_count"])
                / metrics["nrows"]
            ),
            "name": y.name,
            "frequent_elements": {
                "value": labels[:max_num_common_labels],
                "frequency": [float(lc / sum_label_counts) for lc in label_counts[:max_num_common_labels]],
            },
            "insights": insights,
            "metrics": metrics,
        },
        {
            "label_encoder": label_encoder,
            "y_map": y_map,
            "task": task,
            "invalid_row_idxs": np.nonzero(~np.array(valid_rows))[0],
        },
    )


def _analyze_target(y: pd.Series, task: str, metrics: dict):
    # This function includes code that is shared between analyze_target_regression and analyze_target_classification
    y_numpy = y.dropna().to_numpy()
    _verify_y(y_numpy, task)
    y_numpy = y_numpy.astype(str)
    label_encoder = get_label_encoder(task, y_numpy)
    if not isinstance(metrics["labels"], list) or not isinstance(metrics["label_counts"], list):
        unique, counts = unique_without_whitespaces(y_numpy)
        labels = unique.tolist()
        label_counts = counts.tolist()
        sample_size = len(y_numpy)
    else:
        labels = metrics["labels"]
        label_counts = metrics["label_counts"]
        sample_size = metrics["nrows"]
    most_common_label_indexes = np.argsort(-np.array(label_counts))
    labels = np.array(labels)[most_common_label_indexes].astype(str).tolist()
    label_counts = np.array(label_counts)[most_common_label_indexes].astype(int).tolist()
    y_encoded = label_encoder.transform(y.to_numpy().astype(str)).ravel().astype(float)
    y_encoded[pd.isnull(y).to_numpy()] = np.nan
    return label_encoder, labels, label_counts, y_encoded, sample_size


def _verify_y(y: np.array, task: str):
    if task not in [tt.REGRESSION, tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION]:
        raise ValueError(
            "Error: when y is provided task must be REGRESSION, BINARY_CLASSIFICATION or MULTICLASS_CLASSIFICATION"
        )
    if task in [tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION, tt.CLASSIFICATION]:
        if any(value is np.nan for value in y) > 0:
            raise ValueError("Error: nans are not allowed in y for classification task")
        if any(value is None for value in y) > 0:
            raise ValueError("Error: None are not allowed in y for classification task")
