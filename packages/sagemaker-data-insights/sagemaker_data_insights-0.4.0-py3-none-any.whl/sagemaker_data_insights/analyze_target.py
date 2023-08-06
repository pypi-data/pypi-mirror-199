import logging
import pandas as pd
import numpy as np
import scipy

import sagemaker_data_insights.const as cs
from sagemaker_data_insights.const import TaskType as tt
from sagemaker_data_insights.histogram_functions import (
    _verify_y,
    calc_robust_histogram,
    robust_histogram_num_outliers,
    _unique_without_whitespaces,
)
from sagemaker_data_insights.insights import Insights
from sagemaker_data_insights.model_utils import _get_label_encoder

REQUIRED_TARGET_METRICS = {
    "labels",
    "label_counts",
    "cardinality",
    "max",
    "min",
    "numeric_finite_count",
    "nrows",
    "null_like_count",
    "empty_count",
    "whitespace_count",
}


def _check_required_target_metrics_provided(metrics: dict):
    missing_metrics = REQUIRED_TARGET_METRICS - set(metrics.keys())
    if missing_metrics:
        raise ValueError(f"Missing following target metrics: {missing_metrics}")


def analyze_target_regression(
    y: pd.Series, metrics: dict, num_bins: int = 20, max_num_common_labels: int = 10, max_num_outliers: int = 5,
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
    _check_required_target_metrics_provided(metrics)

    label_encoder, labels, label_counts, y_encoded, _ = _analyze_target(y, tt.REGRESSION, metrics)
    valid_rows = np.isfinite(y_encoded).ravel()
    valid_encoded = y_encoded[valid_rows]
    count, bin_edges = np.histogram(valid_encoded, bins=num_bins)
    histogram = {
        "hist_count": count.astype(int).tolist(),
        "hist_edges": bin_edges.astype(float).tolist(),
        "lower_bin_is_outlier": False,
        "upper_bin_is_outlier": False,
    }
    robust_histogram = calc_robust_histogram(valid_encoded, num_bins=num_bins)
    # count outliers to calculate `outliers_ratio`
    num_outliers = robust_histogram_num_outliers(robust_histogram)
    valid_row_idxs = np.nonzero(valid_rows)[0]
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
    outliers_ratio = float(num_outliers / valid_encoded.shape[0])
    skew = float(scipy.stats.skew(valid_encoded.ravel()))
    kurtosis = float(scipy.stats.kurtosis(valid_encoded.ravel()))

    # Check for target insights
    insights = _regression_insights(outliers_ratio, skew, kurtosis, labels, label_counts, metrics)

    return (
        {
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
            "histogram": histogram,
            "robust_histogram": robust_histogram,
            cs.INSIGHTS: insights,
            "metrics": metrics,
        },
        {
            "label_encoder": label_encoder,
            "invalid_row_idxs": np.nonzero(~valid_rows)[0],
            "low_outlier_idxs": low_outlier_idxs,
            "high_outlier_idxs": high_outlier_idxs,
        },
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
    _check_required_target_metrics_provided(metrics)

    try:
        # When the data type of y is string: Null, empty and cells of only whitespace are considered missing
        valid_rows = (~pd.isnull(y)) & (y.str.strip() != "")
    except AttributeError:
        # When the data type of y is not string: only Nulls are considered missing
        valid_rows = ~pd.isnull(y)
    y = y[valid_rows]

    task = tt.BINARY_CLASSIFICATION if len(np.unique(y.to_numpy().astype(str))) == 2 else tt.MULTICLASS_CLASSIFICATION
    label_encoder, labels, label_counts, _, sample_size = _analyze_target(y, task, metrics)
    y_map = {label_encoder.transform([label])[0]: label for label in labels}

    # Check for target insights
    insights = _classification_insights(task, labels, label_counts, sample_size)
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
    label_encoder = _get_label_encoder(task, y_numpy)
    if not isinstance(metrics["labels"], list) or not isinstance(metrics["label_counts"], list):
        unique, counts = _unique_without_whitespaces(y_numpy)
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


def _regression_insights(outliers_ratio, skew, kurtosis, labels, label_counts, metrics):
    insights = []
    if outliers_ratio > 0:
        if abs(skew) > Insights.SKEWED_TARGET_THRESHOLD:
            insights.append(Insights.generate(Insights.SKEWED_TARGET, Insights.HIGH))
        elif kurtosis > Insights.HEAVY_TAILED_TARGET_THRESHOLD:
            insights.append(Insights.generate(Insights.HEAVY_TAILED_TARGET, Insights.HIGH))
        elif kurtosis > Insights.TARGET_OUTLIERS_THRESHOLD:
            insights.append(Insights.generate(Insights.TARGET_OUTLIERS, Insights.MEDIUM))
    majority_label_frequency = label_counts[0] / metrics["nrows"]
    allowed_frequency = Insights.ALLOWED_FREQUENCY_FACTOR / metrics["cardinality"]
    if majority_label_frequency > max(Insights.ALLOWED_FREQUENCY, allowed_frequency):
        insights.append(
            Insights.generate(
                Insights.REGRESSION_FREQUENT_LABEL,
                Insights.MEDIUM,
                {"label": labels[0], "frequency": majority_label_frequency},
            )
        )
    non_numeric_count = metrics["nrows"] - metrics["numeric_finite_count"]
    non_numeric_frequency = non_numeric_count / metrics["nrows"]
    if non_numeric_frequency > 0:
        info = {
            "frequency": non_numeric_frequency,
            "values": list(filter(lambda x: not np.isfinite(pd.to_numeric(x, errors="coerce")), labels))[
                : Insights.NUM_NONUMERIC_LABELS
            ],
        }
        if non_numeric_frequency > Insights.REGRESSION_MANY_NONNUMERIC_THRESHOLD:
            insights.append(Insights.generate(Insights.REGRESSION_MANY_NONNUMERIC, Insights.HIGH, info))
        else:
            insights.append(Insights.generate(Insights.REGRESSION_NONNUMERIC, Insights.MEDIUM, info))
    return insights


def _classification_insights(task, labels, label_counts, sample_size):
    insights = []
    if task == tt.BINARY_CLASSIFICATION:
        for label, count in zip(labels, label_counts):
            if count < Insights.VERY_SMALL_MINORITY_THRESHOLD:
                insights.append(
                    Insights.generate(
                        Insights.VERY_SMALL_MINORITY,
                        Insights.HIGH,
                        {"label": label, "count": count, "sample_size": sample_size, "ratio": count / sample_size},
                    )
                )
    elif task == tt.MULTICLASS_CLASSIFICATION:
        if len(labels) > Insights.HIGH_TARGET_CARDINALITY_THRESHOLD:
            insights.append(
                Insights.generate(Insights.HIGH_TARGET_CARDINALITY, Insights.MEDIUM, {"cardinality": len(labels)})
            )
        else:
            for label, count in zip(labels, label_counts):
                if count <= Insights.RARE_TARGET_LABEL_THRESHOLD:
                    insights.append(
                        Insights.generate(Insights.RARE_TARGET_LABEL, Insights.HIGH, {"label": label, "count": count})
                    )
                elif count < label_counts[0] * Insights.SKEWED_LABEL_FREQUENCY_RATIO:
                    insights.append(
                        Insights.generate(
                            Insights.SKEWED_LABEL_FREQUENCY,
                            Insights.MEDIUM,
                            {
                                "label": label,
                                "count": count,
                                "most_frequent_label": labels[0],
                                "most_frequent_label_count": label_counts[0],
                            },
                        )
                    )
    return insights


# The maximum number of unique labels in a numeric target column to treat the problem as classification.
TASK_TYPE_MAX_NUM_UNIQUES_FOR_NUMERIC_MULTICLASS = 100
# The maximum number of unique labels in a numeric target column under which we always treat the problem as
# regression.
TASK_TYPE_MAX_NUM_UNIQUES_FOR_OBVIOUS_MULTICLASS = 5
# By how many times the target column's maximum should exceed the number of labels to treat the column as ordinal.
TASK_TYPE_MAX_NUM_UNIQUES_MULTIPLE_FOR_ORDINAL = 10
# The minimum fraction of values which should be numeric for the target to be treated as numeric.
TASK_TYPE_MIN_FRACTION_FOR_NUMERIC = 0.5
# The minimum value that #uniques / #rows should be to allow regression when the labels are mostly integers.
TASK_TYPE_MIN_FRACTION_INTEGER_UNIQUES_FOR_REGRESSION = 0.015
# The minimum fraction of values which should be non-integer floats in order to treat the problem as regression.
TASK_TYPE_MIN_FRACTION_NONINTEGER_FLOATS_FOR_REGRESSION = 0.01
# Maximum number of supported classes for multiclass classification problems.
TASK_TYPE_MAX_NUM_SUPPORTED_CLASSES = 2000


def determine_task(metrics: dict):
    """Determines the problem type based on basic statistics about the target column.
    - The logic is copied from `determine_task` of AIAlgorithmsPipelineRecommender

    Parameters
    ----------
    metrics : dict
        must include all the following keys calculated on the target column: `cardinality`, `integer_count`, `max`,
        `min`, `numeric_finite_count` and `nrows`. Keys definitions can be found in const.py.

    Returns
    -------
    str: The identified problem type in [tt.REGRESSION, tt.BINARY_CLASSIFICATION, tt.MULTICLASS_CLASSIFICATION]
    """
    cardinality = metrics["cardinality"]
    num_integers = metrics["integer_count"]
    num_numeric_finite = metrics["numeric_finite_count"]
    num_rows = metrics["nrows"]
    target_max = metrics["max"]
    target_min = metrics["min"]

    # These guarantees should be in place before this function is called.
    assert num_rows > 0, "Cannot determine problem type with no rows sampled."
    assert cardinality >= 2, f"Cannot determine problem type from target column with {cardinality} unique values."

    if cardinality == 2:
        logging.info("determine_task, task = %s", tt.BINARY_CLASSIFICATION)
        return tt.BINARY_CLASSIFICATION

    if num_numeric_finite > TASK_TYPE_MIN_FRACTION_FOR_NUMERIC * num_rows:
        # Target column is mostly numeric.

        if cardinality <= TASK_TYPE_MAX_NUM_UNIQUES_FOR_OBVIOUS_MULTICLASS:
            # When there are not many labels, use multiclass classification even if the labels are non-integer floats.
            logging.info("determine_task, task = %s", tt.MULTICLASS_CLASSIFICATION)
            return tt.MULTICLASS_CLASSIFICATION

        fraction_noninteger_floats = 1 - (num_integers / num_numeric_finite)
        if fraction_noninteger_floats >= TASK_TYPE_MIN_FRACTION_NONINTEGER_FLOATS_FOR_REGRESSION:
            # Most of the values are non-integer floats.
            logging.info("determine_task, task = %s", tt.REGRESSION)
            return tt.REGRESSION

        ordinal_encoded = target_min >= 0 and target_max <= cardinality * TASK_TYPE_MAX_NUM_UNIQUES_MULTIPLE_FOR_ORDINAL
        if not ordinal_encoded and (cardinality / num_rows) >= TASK_TYPE_MIN_FRACTION_INTEGER_UNIQUES_FOR_REGRESSION:
            # The spread of labels is very wide, so treat the problem as regression despite mostly integer labels.
            logging.info("determine_task, task = %s", tt.REGRESSION)
            return tt.REGRESSION

        if cardinality <= TASK_TYPE_MAX_NUM_UNIQUES_FOR_NUMERIC_MULTICLASS:
            # Values are mostly integers, and there are not too many labels.
            logging.info("determine_task, task = %s", tt.MULTICLASS_CLASSIFICATION)
            return tt.MULTICLASS_CLASSIFICATION

        raise ValueError(
            f"It is unclear whether the problem type should be {tt.MULTICLASS_CLASSIFICATION} or {tt.REGRESSION}."
            f" Please specify the problem type manually and retry."
        )

    # Target is mostly non-numeric.

    if cardinality <= TASK_TYPE_MAX_NUM_SUPPORTED_CLASSES:
        # Less than half of the labels are numeric, and there are not "too many" distinct values.
        logging.info("determine_task, task = %s", tt.MULTICLASS_CLASSIFICATION)
        return tt.MULTICLASS_CLASSIFICATION

    # There are too many distinct values for multiclass-classification.
    raise ValueError(
        f"The number of unique labels {cardinality} is larger than the maximum number of supported classes of"
        f" {TASK_TYPE_MAX_NUM_SUPPORTED_CLASSES}. Please verify that the target column is set correctly and retry."
    )
