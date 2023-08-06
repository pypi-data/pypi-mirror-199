from enum import Enum
import numpy as np
import pandas as pd

from sagemaker_data_insights.insights import Insights
from sagemaker_data_insights.const import TaskType as tt


def regression_insights(outliers_ratio, skew, kurtosis, labels, label_counts, metrics):
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


def classification_insights(task, labels, label_counts, sample_size):
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
                elif count < label_counts[0] * Insights.IMBALANCED_CLASS_RATIO:
                    insights.append(
                        Insights.generate(
                            Insights.IMBALANCED_CLASSES,
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


class ModelInsightsConstraint(Enum):
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
