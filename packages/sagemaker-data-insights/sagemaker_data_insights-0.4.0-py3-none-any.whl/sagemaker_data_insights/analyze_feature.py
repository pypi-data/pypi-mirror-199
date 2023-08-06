import pandas as pd
import numpy as np
import re
import scipy
import logging

import sagemaker_data_insights.const as cs
from sagemaker_data_insights.const import FeatureType as ft
from sagemaker_data_insights.const import TaskType as tt
from sagemaker_data_insights.insights import Insights
from sagemaker_data_insights.histogram_functions import (
    calc_frequent_elements,
    calc_robust_histogram,
    robust_histogram_num_outliers,
)


def missing_ratio(metrics: dict):
    return float((metrics["null_like_count"] + metrics["empty_count"] + metrics["whitespace_count"]) / metrics["nrows"])


def valid_ratio(metrics: dict, feature_type: str):
    if feature_type == ft.NUMERIC:
        return float(metrics["numeric_finite_count"] / metrics["nrows"])
    elif feature_type in [ft.CATEGORICAL, ft.BINARY, ft.TEXT]:
        return float(
            (metrics["nrows"] - metrics["null_like_count"] - metrics["empty_count"] - metrics["whitespace_count"])
            / metrics["nrows"]
        )
    elif feature_type == ft.DATETIME:
        return float(metrics["datetime_count"] / metrics["datetime_rows_parsed"])
    elif feature_type == ft.VECTOR:
        return 1 - missing_ratio(metrics)
    raise ValueError(f"Unsupported feature type {feature_type}")


def _numpy_conversion(x: pd.Series, y: pd.Series):
    """
    Converts original pandas column data to numpy and excludes null value.

    Parameters
    ----------
    x : pandas.Series
        raw column data
    y : pandas.Series or Nones
        raw target column data(if any)

    Returns
    -------
    x_numpy : np.ndarray
              Non-null x in numpy
    y_numpy : None or np.ndarray
              None if y is None, otherwise non-null y in numpy
    """
    x_numpy = x.to_numpy().reshape((-1, 1))
    valid_idxs = ~pd.isnull(x_numpy)
    x_numpy = x_numpy[valid_idxs].astype(str).reshape((-1, 1))
    y_numpy = None if y is None else y.to_numpy().reshape((-1, 1))[valid_idxs].reshape((-1, 1))
    return x_numpy, y_numpy


def get_feature_transform_and_transformed_x(feature_type: str, x_numpy: np.ndarray):
    """
    Gets the default feature transform used by data_insights and applys it to input numpy array.

    Parameters
    ----------
    feature_type : str
    x_numpy : np.ndarray

    Returns
    -------
    feature_transform : Default feature transform used by data_insights
    x_transformed : x after applying feature transfor

    """
    from sagemaker_data_insights.utils.feature_transform import get_feature_transform
    feature_transform = get_feature_transform(feature_type, True).fit(x_numpy)
    x_transformed = feature_transform.transform(x_numpy)
    return feature_transform, x_transformed


def analyze_feature(  # noqa: C901
    x: pd.Series,
    y: pd.Series,
    task: str,
    feature_type: str,
    metrics: dict,
    num_bins: int = 20,
    random_state: int = 0,
    n_jobs: int = 1,
    requested_stats: list = None,
):
    """
    Feature analyzer. Provides ML relevant statistics about the feature. Different statistics will be derived for each
    feature type.

    Parameters
    ----------
    x : pandas.Series
        raw feature column vector (e.g. NOT encoded using one hot encoder)
    y : pandas.Series or None
        (When y is not provided, all statistics that depend on the target column are not calculated)
        Encoded and clean target column. For regression, all values must be finite floats (np.nan are not allowed).
        For classification, the labels must be encoded as numeric integers consecutive and starting from 0. For both
        regression and classification, it's recommended to use the label_encoder provided by `analyze_target_regression`
        or `analyze_target_classification` to encode the target column. Note that `analyze_target_regression` returns
        a list of invalid row indexes that must be removed from the data before calling `_baseline_prediction_power`
    task : str or None (must be provided when y is provided)
        REGRESSION, BINARY_CLASSIFICATION or MULTICLASS_CLASSIFICATION
    feature_type: str
        NUMERIC, CATEGORICAL, TEXT, DATETIME or BINARY. If unknown, use `get_feature_type`
    metrics : dictionary that must include all the following keys: nrows, numeric_finite_count, cardinality and
        empty_count. See the descriptions in const.py
    num_bins : int >= 3
        number of bins to use in histograms. In some cases, this is used as the decision threshold between producing a
        histogram or frequent values: When there are more unique values than `num_bins` then a histogram is produced,
        otherwise - frequent values.
    random_state : int
        random seed
    n_jobs : int
        number of cores for XGBoost in _calc_prediction_power
    requested_stats : list of strings or None
        Possible values:
            None - return the default set of stats
            ['only_prediction_power'] - returns only prediciton power
        Additional values are:
        'text_stats' which return the default set of stats and the additionaly requested stats.
        For example: ['text_stats']

    Returns
    -------
    dict: data insights metrics. Statistics will be derived according to the provided feature type. The fields with *
    are derived from the provided metrics, all other - from x and y
        All feature types:
            name: feature name taken from x
            type: feature type provided in the input
            metrics*: metrics dict provided in the input
            prediction_power and normalized_prediction_power: available when y and task are provided
            frequent_elements: calculated using histogram_functions.calc_frequent_elements
            missing_ratio*: ratio of number of null like and empty rows to the number of rows
            {cs.INSIGHTS}: list of insights. Can include: TARGET_LEAKAGE, UNINFORMATIVE_FEATURE,
                NUMERIC_DISGUISED_MISSING_VALUE, CATEGORICAL_RARE_CATEGORIES
        Numeric:
            robust_histogram: calculated using histogram_functions.calc_robust_histogram
            histogram: calculated using numpy.histogram
            outliers_ratio: ratio of the number of outliers to number of samples
            skew: calculated using scipy.stats.skew
            kurtosis: calculated using scipy.stats.kurtosis
            valid_ratio*: ratio of the number of finite numeric values to the number of samples
        Categorical / Binary:
            valid_ratio*: ratio of the number of not null like values and not whitespace strings to the number of
                samples
        Text:
            valid_ratio*: ratio of the number of not null like values and not whitespace strings to the number of
                samples
            important_words: for each word prediction_power, normalized_prediction_power and frequency
            character_statistics: dictionary with character statistics. For each statistic a dictionary with
                prediction_power, normalized_prediction_power and either robust_histogram or frequent_elements. The
                possible character statistics are:
                    word_count: number of words
                    char_count: string length
                    special_ratio: ratio of non alphanumeric characters to non-spaces in the string, 0 if empty string
                    digit_ratio: ratio of digits characters to non-spaces in the string, 0 if empty string
                    lower_ratio: ratio of lowercase characters to non-spaces in the string, 0 if empty string
                    capital_ratio: ratio of uppercase characters to non-spaces in the string, 0 if empty string
                Note that some of them could be missing if there's only one value. For example, word_count will be
                missing if all texts contain exactly one word.
        Datetime:
            valid_ratio: ratio of number valid datetime values to the number of samples
            datetime_features: dict. Prediction power and robust histogram or frequent elements stats for each of the
                following: "month", "hour", "weekday", "year", "minute", "second", "week". Note that some items could
                be missing if there is no relevant data in the feature
    """
    if y is not None and task is None:
        raise ValueError("Task must be specified when y is provided")
    if feature_type not in [ft.NUMERIC, ft.CATEGORICAL, ft.TEXT, ft.DATETIME, ft.BINARY, ft.VECTOR]:
        raise ValueError(
            f"feature_type must be one of {ft.NUMERIC}, {ft.CATEGORICAL}, {ft.TEXT}, {ft.DATETIME}, {ft.BINARY} or "
            f"{ft.VECTOR}"
        )
    if requested_stats is not None:
        for rs in requested_stats:
            assert rs in ["only_prediction_power", "text_stats", "text_patterns"]
        if "only_prediction_power" in requested_stats and len(requested_stats) > 1:
            raise ValueError(
                f"Other stats are not allowed when requested_stats contains only_prediction_power. Requested_stats "
                f"is {requested_stats}"
            )
    assert task is None or task in [tt.REGRESSION, tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION]
    x_numpy, y_numpy = _numpy_conversion(x, y)
    # transform the feature using a default transform for this feature_type. The transformed featured is used to derive
    # some statistics. For example: prediction power
    # Statistics relevant to all feature types
    insights = {
        "name": x.name,
        "type": feature_type,
        "metrics": metrics,
    }
    if len(x_numpy) == 0:
        insights["missing_ratio"] = 1
        insights["valid_ratio"] = 0
        insights["frequent_elements"] = []
        insights[cs.INSIGHTS] = []
        return insights

    feature_transform, x_transformed = get_feature_transform_and_transformed_x(feature_type, x_numpy)

    if y is not None:
        from sagemaker_data_insights.model_utils import _calc_prediction_power
        insights["prediction_power"], insights["normalized_prediction_power"] = _calc_prediction_power(
            x_transformed, y_numpy, task, random_state, n_jobs=n_jobs
        )
    if requested_stats is not None and "only_prediction_power" in requested_stats:
        return insights

    insights["frequent_elements"] = calc_frequent_elements(x_numpy, y_numpy, task)
    insights["missing_ratio"] = missing_ratio(metrics)

    # Add insights and statistics specific for each feature type
    insights.update(
        {
            ft.NUMERIC: lambda: _analyze_numeric_feature(
                x_transformed, y_numpy, metrics, task, insights["frequent_elements"], num_bins
            ),
            ft.TEXT: lambda: _analyze_text_feature(
                x_numpy, y_numpy, metrics, task, num_bins, n_jobs, requested_stats=requested_stats
            ),
            ft.DATETIME: lambda: _analyze_datetime_feature(
                feature_transform, x_transformed, y_numpy, metrics, task, num_bins, random_state
            ),
            ft.BINARY: lambda: _analyze_binary_feature(metrics),
            ft.CATEGORICAL: lambda: _analyze_categorical_feature(insights["frequent_elements"], metrics),
            ft.VECTOR: lambda: _analyze_vector_feature(metrics),
        }[feature_type]()
    )

    # Insights relevant to all feature types
    if "normalized_prediction_power" in insights:
        if insights["normalized_prediction_power"] > Insights.TARGET_LEAKAGE_THRESHOLD:
            insights[cs.INSIGHTS].append(Insights.generate(Insights.TARGET_LEAKAGE, Insights.HIGH))
        elif insights["normalized_prediction_power"] <= Insights.UNINFORMATIVE_FEATURE_THRESHOLD:
            insights[cs.INSIGHTS].append(Insights.generate(Insights.UNINFORMATIVE_FEATURE, Insights.LOW))
    if len(insights["frequent_elements"]["frequency"]) == 1:
        insights[cs.INSIGHTS].append(Insights.generate(Insights.CONSTANT_FEATURE, Insights.LOW))
    return insights


def get_valid_transformed_data(x_transformed: np.array, y: np.array):
    valid_idxs = np.isfinite(x_transformed)
    y_valid = None if y is None else y[valid_idxs].ravel()
    x_transformed_valid = x_transformed[valid_idxs]
    return valid_idxs, y_valid, x_transformed_valid


def _analyze_numeric_feature(
    x_transformed: np.array, y: np.array, metrics: dict, task: str, frequent_elements: dict, num_bins: int
):
    valid_idxs, y_valid, x_transformed_valid = get_valid_transformed_data(x_transformed, y)
    robust_histogram = calc_robust_histogram(x_transformed_valid.ravel(), y_valid, task=task, num_bins=num_bins)
    num_outliers = robust_histogram_num_outliers(robust_histogram)
    count, bin_edges = np.histogram(x_transformed_valid.ravel(), bins=num_bins)
    histogram = {
        "hist_count": count.astype(int).tolist(),
        "hist_edges": bin_edges.astype(float).tolist(),
        "lower_bin_is_outlier": False,
        "upper_bin_is_outlier": False,
    }

    # insights for numeric feature
    insights = []
    if (
        frequent_elements["frequency"][0] > Insights.NUMERIC_DISGUISED_THRESHOLD
        and len(frequent_elements["frequency"]) > 1
        and frequent_elements["frequency"][0] > Insights.NUMERIC_DISGUISED_RATIO * frequent_elements["frequency"][1]
        and str(frequent_elements["value"][0]).isnumeric()
        and metrics["cardinality"] > Insights.NUMERIC_DISGUISED_MIN_UNIQUE
    ):
        insights.append(
            Insights.generate(
                Insights.NUMERIC_DISGUISED_MISSING_VALUE,
                Insights.MEDIUM_FEATURE,
                {"value": frequent_elements["value"][0], "frequency": frequent_elements["frequency"][0]},
            )
        )
    return {
        "robust_histogram": robust_histogram,
        "histogram": histogram,
        "outliers_ratio": float(num_outliers / sum(valid_idxs)),
        "skew": float(scipy.stats.skew(x_transformed_valid.ravel())),
        "kurtosis": float(scipy.stats.kurtosis(x_transformed_valid.ravel())),
        "valid_ratio": valid_ratio(metrics, ft.NUMERIC),
        cs.INSIGHTS: insights,
    }


def _analyze_categorical_feature(frequent_elements: dict, metrics: dict):
    insights = []
    if len(frequent_elements["frequency"]) == 0:  # The column contains only missing values
        return {"valid_ratio": 0, cs.INSIGHTS: insights}
    normalized_frequency = np.array(frequent_elements["frequency"]) / frequent_elements["frequency"][0]
    num_rare_categories = sum(normalized_frequency < Insights.CATEGORICAL_RARE_CATEGORIES_THRESHOLD)
    if num_rare_categories > 2:
        rare_categories = list(np.array(frequent_elements["value"])[normalized_frequency < 0.05])
        rare_categories_frequency = list(np.array(frequent_elements["frequency"])[normalized_frequency < 0.05])
        insights.append(
            Insights.generate(
                Insights.CATEGORICAL_RARE_CATEGORIES,
                Insights.MEDIUM_FEATURE,
                {"rare_categories": rare_categories, "rare_categories_frequency": rare_categories_frequency},
            )
        )
    return {
        "valid_ratio": valid_ratio(metrics, ft.CATEGORICAL),
        cs.INSIGHTS: insights,
    }


def _analyze_binary_feature(metrics: dict):
    return {
        "valid_ratio": valid_ratio(metrics, ft.BINARY),
        cs.INSIGHTS: [],
    }


def _analyze_datetime_feature(
    feature_transform, x_transformed: np.array, y: np.array, metrics: dict, task: str, num_bins: int, random_state=0
):
    datetime_features = {}
    # go over the internal features produced by the feature_transform e.g. week, month, hour etc.
    for idx, e in enumerate(feature_transform.extract_):
        col = x_transformed[:, idx].reshape((-1, 1))
        valid_rows = np.isfinite(col)
        col = col[valid_rows].reshape((-1, 1))
        internal_feature_insights = {}
        assert e.extract_func.__name__[:8] == "extract_"
        internal_feature_name = e.extract_func.__name__[8:]  # remove `extract_` from the head of the string
        if y is not None:
            from sagemaker_data_insights.model_utils import _calc_prediction_power
            y_valid = y[valid_rows].reshape((-1, 1))
            (
                internal_feature_insights["prediction_power"],
                internal_feature_insights["normalized_prediction_power"],
            ) = _calc_prediction_power(col, y_valid, task, random_state)
        else:
            y_valid = None
        # Some internal feature types should always be frequent elements. For others, they are frequent elements when
        # they contain few unique elements or histogram when they contain many unique elements
        if internal_feature_name in ["quarter", "month", "hour", "weekday"] or len(np.unique(col)) <= num_bins:
            internal_feature_insights["frequent_elements"] = calc_frequent_elements(
                col.astype(int), y_valid, task=task, sort_type="value", max_num_elements=len(np.unique(col))
            )
        else:
            internal_feature_insights["robust_histogram"] = calc_robust_histogram(
                col, y_valid, task=task, num_bins=num_bins
            )
        datetime_features[internal_feature_name] = internal_feature_insights
    return {
        "valid_ratio": valid_ratio(metrics, ft.DATETIME),
        "datetime_features": datetime_features,
        cs.INSIGHTS: [],
    }


def _analyze_text_feature(  # noqa: C901
    x: np.array,
    y: np.array,
    metrics: dict,
    task: str,
    num_bins: int,
    random_state: int = 0,
    n_jobs: int = 1,
    num_top_words: int = 200,
    requested_stats: list = None,
):
    """
    Derive statistics and insights specific to text features.

    Parameters
    ----------
    x : np.ndarray of size (height, 1)
        text feature
    y : np.ndarray of size (height, 1)
        clean and encoded target column. See the documentation in `analyze_feature`
    metrics : dictionary
        See the documentation in `analyze_feature`
    task : str or None (must be provided when y is provided)
        REGRESSION, BINARY_CLASSIFICATION or MULTICLASS_CLASSIFICATION
    num_bins : int >= 3
        number of bins to use in histograms. In some cases, this is used as the decision threshold between producing a
        histogram or frequent values: When there are more unique values than `num_bins` then a histogram is produced,
        otherwise - frequent values.
    random_state: int
        random seed used for RNG
    n_jobs : int
        number of cores for XGBoost in _calc_prediction_power
    num_top_words: int
        max number of most important words to return, see `from important_words` below
    requested_stats : list of strings or None
        Possible values:
            * 'text_stats' for statistics on the distrbution of characters and tokens
            * 'text_patterns' for results of an analysis of textual patterns

    Returns
    -------
    dict: text feature insights. See analyze_feature
"""
    x_list = list(x.ravel())
    insights = {
        "valid_ratio": valid_ratio(metrics, ft.TEXT),
        cs.INSIGHTS: [],
        "character_statistics": {},
    }

    if not requested_stats:
        return insights

    if "text_stats" in requested_stats:
        from sagemaker_data_insights.text_utils import CharacterStatistics
        # Numeric character statistics: from every string extract various ratio and count statistics. These are numeric
        # features that capture various characteristics of the string
        for desc, func in CharacterStatistics.functions.items():
            feat = np.vectorize(func)(x_list).reshape((-1, 1))
            num_unique = len(np.unique(feat))
            if num_unique <= 1:
                continue
            feat_stats = {}

            if y is not None:
                from sagemaker_data_insights.model_utils import _calc_prediction_power
                feat_stats["prediction_power"], feat_stats["normalized_prediction_power"] = _calc_prediction_power(
                    feat, y, task, random_state, n_jobs=n_jobs
                )
            if num_unique > num_bins:
                feat_stats["robust_histogram"] = calc_robust_histogram(feat, y, task, num_bins=num_bins)
            else:
                feat_stats["frequent_elements"] = calc_frequent_elements(
                    feat, y, task, max_num_elements=num_bins, sort_type="value"
                )
            insights["character_statistics"][desc] = feat_stats

        from sagemaker_data_insights import text_utils
        # token importance: add information about token importance when tokenizing based on words
        insights["important_words"] = text_utils.token_importance(
            x, y, task, random_state=random_state, analyzer="word", n_jobs=n_jobs, num_top_features=num_top_words
        )

    if "text_patterns" in requested_stats:
        from sagemaker_data_insights.patterns.analyze_patterns import analyze_text_patterns
        expression_set = analyze_text_patterns(x.reshape(-1), min_coverage=0.8, random_state=random_state)
        num_experiments, sample_size = expression_set.experiment_statistics()

        pattern_columns = ["Pattern", "Relevance", "Regular expression", "Matches", "Non-matches"]
        pattern_dict = {k: [] for k in pattern_columns}

        for expr in expression_set.ranked_expressions():
            pattern = expr.annotated_str()
            confidence = expr.coverage_accumulator.value()

            # Surround matches and nonmatches with angle brackets to show whitespace.
            matches = _sanitize_strings(expr.matches_histogram.top_n(5))
            nonmatches = _sanitize_strings(expr.outliers_histogram.top_n(5))

            num_rows = max(len(matches), len(nonmatches))
            padding = [""] * (num_rows - 1)

            pattern_dict["Pattern"].extend([pattern] + padding)
            # Our external language for accuracy/confidence is 'Relevance'.
            pattern_dict["Relevance"].extend(["{:.2f}".format(100 * confidence)] + padding)
            pattern_dict["Regular expression"].extend([expr.regex(use_token_lengths=True)] + padding)
            pattern_dict["Matches"].extend(matches + [""] * (num_rows - len(matches)))
            pattern_dict["Non-matches"].extend(nonmatches + [""] * (num_rows - len(nonmatches)))

            if confidence < 1 and confidence >= Insights.HIGH_CONFIDENCE_PATTERN_THRESHOLD:
                insights[cs.INSIGHTS].append(
                    Insights.generate(
                        Insights.HIGH_CONFIDENCE_PATTERN,
                        Insights.MEDIUM,
                        {
                            "pattern": pattern,
                            "confidence": confidence,
                            "num_experiments": num_experiments,
                            "sample_size": sample_size,
                        },
                    )
                )

        # If there are no patterns, return a table with a single column and an informative message.
        if expression_set.best_expression() is None:
            pattern_columns = ["Pattern"]
            pattern_dict = {"Pattern": ["No textual patterns found."]}

        pattern_df = pd.DataFrame(columns=pattern_columns, data=pattern_dict)
        insights["text_patterns"] = pattern_df.to_dict()

    return insights


def _show_whitespace(str):
    """Replaces leading and trailing whitespace with tokens. Additionally tokenizes an empty string."""
    if str == "":
        return "{empty string}"

    WHITESPACE = "{whitespace}"
    str = re.sub(r"^\s+", WHITESPACE, str)
    str = re.sub(r"\s+$", WHITESPACE, str)

    return str


def _sanitize_strings(strs):
    # Replace leading an trailing whitespace with tokens.
    strs = [_show_whitespace(s) for s in strs]
    # Deduplicate strings while maintaining initial order.
    return list(dict.fromkeys(strs))


def _analyze_vector_feature(metrics):
    return {
        "valid_ratio": valid_ratio(metrics, ft.VECTOR),
        cs.INSIGHTS: [],
    }


def get_feature_type(metrics: dict, allowed_types: list = None, prefer_categorical=False):
    """
    Feature type analyzer

    Parameters
    ----------
    metrics : dict
        must include all the following keys: `median`, `numeric_finite_count`, `nrows`, `null_like_count`,
        `empty_count`, `whitespace_count`, `cardinality`, `datetime_count`, `datetime_non_float_count` and
        `datetime_rows_parsed`. Keys definitions can be found in const.py. While `x` is usually a sample of the data,
        the metrics should be calculated on the whole data or on a larger sample.
    allowed_types: list(str)
        List of allowed feature types. Can include the following types from const.py: NUMERIC, CATEGORICAL, TEXT,
        DATETIME, BINARY. By default includes all.
    prefer_categorical: bool
        Prefer categorical types to numerical types in case of ties.

        TODO. This flag is being used for Ganymede and will be tested for use as
        a default option in Data Insights. If it becomes a default option,
        consumers of data insights will need to do regression tests when they
        upgrade to the 2.0 branch (this branch).

    Returns
    -------
    str: feature type
        The type with the highest probability out of the types allowed in `allowed_types`
    dict: feature type probabilities
        The probability for the feature to be each of the types NUMERIC, CATEGORICAL, TEXT, DATETIME, BINARY. Type not
        included in `allowed_types` will have a zero probability
"""
    # TODO: add detection of ft.VECTOR copy logic from
    #  https://code.amazon.com/packages/AIAlgorithmsDataInsights/commits/081735f1f34b8c8ea7e24f76c390f84036f98e84

    # The order of all_types is used to break ties
    # the types are ordered by importance.
    if prefer_categorical:
        all_types = [ft.BINARY, ft.CATEGORICAL, ft.NUMERIC, ft.TEXT, ft.DATETIME]
    else:
        all_types = [ft.BINARY, ft.NUMERIC, ft.CATEGORICAL, ft.TEXT, ft.DATETIME]

    if not allowed_types:
        allowed_types = all_types
    else:
        for t in allowed_types:
            if t not in all_types:
                raise ValueError(f"Error: type {t} is not allowed. Allowed types: {allowed_types}")
    probs = _calculate_schema_probs(
        allowed_types,
        metrics["median"],
        metrics["numeric_finite_count"],
        metrics["nrows"],
        metrics["null_like_count"],
        metrics["empty_count"],
        metrics["whitespace_count"],
        metrics["cardinality"],
        metrics["datetime_count"],
        metrics["datetime_non_float_count"],
        metrics["datetime_rows_parsed"],
    )

    # We will use the column type with the highest score, breaking ties using
    # binary > numeric > categorical > text > datetime unless prefer_categorical is set, in which case we use
    # binary > categorical > numeric > text > datetime to break ties.
    score_type_pairs = [(probs[key], key) for key in all_types]
    score_type_pairs.sort(key=lambda x: -x[0])  # This sort is stable, so will preserve order above on ties
    _, col_type = score_type_pairs[0]
    return col_type, probs


def _calculate_schema_probs(  # noqa: C901
    allowed_types,
    median,
    numeric_finite_count,
    nrows,
    null_like_count,
    empty_count,
    whitespace_count,
    cardinality,
    datetime_count,
    datetime_non_float_count,
    datetime_rows_parsed,
):
    """
    Calculates the probabilities for the feature to be any of the types of `schema_types` based on a set of heuristic
    rules

    Parameters
    ----------
    allowed_types: list(str)
        List of allowed feature types. Can include the following types from const.py: NUMERIC, CATEGORICAL, TEXT,
        DATETIME, BINARY. By default includes all.
    median: see description in `const.py`
    numeric_finite_count: see description in `const.py`
    nrows: see description in `const.py`
    null_like_count: see description in `const.py`
    empty_count: see description in `const.py`
    whitespace_count: see description in `const.py`
    cardinality: see description in `const.py`
    datetime_count: see description in `const.py`
    datetime_non_float_count: see description in `const.py`
    datetime_rows_parsed: see description in `const.py`

    Returns
    -------
    dict: feature type probabilities
        The probability for the feature to be each of the types NUMERIC, CATEGORICAL, TEXT, DATETIME, BINARY. Type not
        included in `allowed_types` will have a zero probability
"""
    # Initialize all types to zero
    numeric = 0
    categorical = 0
    text = 0
    datetime = 0
    binary = 0

    # Probability-like score of column being numeric is proportional to the fraction of entries castable to float.
    if ft.NUMERIC in allowed_types and not np.isnan(median):
        numeric = numeric_finite_count / (nrows - null_like_count - empty_count - whitespace_count)

    # Probability-like score of column being text is proportional to the fraction of non-numeric, non-empty entries.
    if ft.TEXT in allowed_types:
        text_like_rows = nrows - numeric_finite_count - null_like_count - empty_count - whitespace_count
        text = text_like_rows / nrows

    if cardinality == 2:
        if ft.BINARY in allowed_types:
            binary = 1.0
            text = 0.0
        if ft.CATEGORICAL in allowed_types:
            categorical = 1.0
            text = 0.0
    elif ft.CATEGORICAL in allowed_types:
        categorical_ratio = cardinality / nrows
        if categorical_ratio < 0.01:
            # If there are on average more than 1/.01 = 100 entries per category, use full categorical and disable text.
            categorical = 1.0
            text = 0.0
        elif 0.01 <= categorical_ratio < 0.2:
            # If there are on average fewer than 1/.01 = 100 but more than 1/.2 = 5 entries per category,
            # then proportionally decrease probability to zero.
            categorical = 1 - (categorical_ratio - 0.01) / 0.19
        else:
            # Don't count as categorical if on average there are fewer than 5 entries per category.
            categorical = 0.0

    if (
        ft.DATETIME in allowed_types
        and datetime_non_float_count / datetime_rows_parsed > 0.05
        and datetime_count / datetime_rows_parsed > 0.6
    ):
        datetime = 1.0
        text = 0.0
        categorical = 0.0
        numeric = 0.0

    # Normalize so that scores sum to 1.
    normalizing_sum = numeric + categorical + text + datetime + binary
    if normalizing_sum == 0:
        raise ValueError(f"Error: scores for all allowed types are zero. Allowed types: {allowed_types}")
    numeric = numeric / normalizing_sum
    categorical = categorical / normalizing_sum
    text = text / normalizing_sum
    datetime = datetime / normalizing_sum
    binary = binary / normalizing_sum

    return {ft.NUMERIC: numeric, ft.CATEGORICAL: categorical, ft.TEXT: text, ft.DATETIME: datetime, ft.BINARY: binary}
