########################################################################################################################
# Metrics definitions
########################################################################################################################
# Unique values stats:
#   labels & label_counts: list of all labels in the column with their counts (np.nan is also accepted, then labels and
#       label_counts will be calculated using the provided data)
#   cardinality: number of unique values in the column
# Numeric stats:
#   max: maximum numeric value (np.nan if no numeric values exist)
#   min: minimum numeric value (np.nan if no numeric values exist)
#   median: median of numeric values (np.nan if no numeric values exist)
#   mean: mean of numeric values (np.nan if no numeric values exist)
# Counts:
#   nrows: number of rows (entries) in the column
#   numeric_finite_count: number of entries that contain numeric finite values
#   integer_count: number of entries that contain integers
#   null_like_count: number of entries that contain null like values
#   empty_count: number of empty rows (entries)
#   whitespace_count: number of rows (entries) than contain only white spaces. Empty string are not counted
#   datetime_count: number of rows (entries) in the column that could be parsed as datetime
#   datetime_non_float_count: number of rows (entries) in the column that could be parsed as datetime but not as numeric
#   datetime_rows_parsed: number of rows (entries) in the column used by datetime parser. As datetime parser is slow, in
#       some cases we run it on a smaller sample


class TaskType:
    REGRESSION = "Regression"
    CLASSIFICATION = "Classification"  # can be either BINARY_CLASSIFICATION or MULTICLASS_CLASSIFICATION
    BINARY_CLASSIFICATION = "BinaryClassification"
    MULTICLASS_CLASSIFICATION = "MulticlassClassification"


class FeatureType:
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    TEXT = "text"
    DATETIME = "datetime"
    BINARY = "binary"
    VECTOR = "vector"


class DeequFeatureType:
    FRACTIONAL = "Fractional"
    INTEGRAL = "Integral"
    STRING = "String"
    TEXT = "String"
    UNKNOWN = "Unknown"
    BOOLEAN = "Boolean"


QUICK_MODEL_METRICS = {
    TaskType.REGRESSION: [
        "r2",
        "neg_mean_squared_error",
        "neg_mean_absolute_error",
        "neg_root_mean_squared_error",
        "max_error",
        "explained_variance",
        "neg_median_absolute_error",
    ],
    TaskType.BINARY_CLASSIFICATION: ["roc_auc", "f1", "accuracy", "balanced_accuracy", "precision", "recall"],
    TaskType.MULTICLASS_CLASSIFICATION: [
        "accuracy",
        "balanced_accuracy",
        "roc_auc_ovr",
        "roc_auc_ovo",
        "roc_auc_ovr_weighted",
        "roc_auc_ovo_weighted",
        "f1_micro",
        "f1_macro",
        "f1_weighted",
        "precision_micro",
        "precision_macro",
        "precision_weighted",
        "recall_micro",
        "recall_macro",
        "recall_weighted",
    ],
}

QUICK_MODEL_BASE_METRICS = {
    TaskType.REGRESSION: "r2",
    TaskType.BINARY_CLASSIFICATION: "roc_auc",
    TaskType.MULTICLASS_CLASSIFICATION: "accuracy",
}

########################################################################################################################
# Cross Column Insights Keys
########################################################################################################################
# Cross Column Insights
PEARSON = "pearson"
ALLOWED_CROSS_COL_INSIGHTS = [PEARSON]
# Input Feature Set Keys
FEATURE_TYPES = "feature_types"
FEATURE_DATA = "feature_data"

########################################################################################################################
# Keys
########################################################################################################################
INSIGHTS = "insights"  # This is a key used for a vector of insights. The insights are listed in `insights.py`
