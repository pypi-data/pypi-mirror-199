# Column data insights constants
VALUE = "value"
COUNT = "count"
DATA = "data"


class HistogramParamsKeys:
    HIST_MAX_BIN_NUM = 24
    HIST_COUNT = "hist_count"
    HIST_EDGES = "hist_edges"
    UPPER_BIN_IS_OUTLIER = "upper_bin_is_outlier"
    LOWER_BIN_IS_OUTLIER = "lower_bin_is_outlier"
    MIN_VALUE = "minValue"
    MAX_VALUE = "maxValue"
    IS_OUTLIER = "isOutlier"


class CategoricalParamsKeys:
    DISTINCT_VALUES = "distinctValues"
    OTHER = "Other categories"


class ColumnDataInsightsParamsKeys:
    COLUMN_NAME = "columnName"
    LOGICAL_DATA_TYPE = "logicalDataType"
    VALID_RATIO = "validRatio"
    INVALID_RATIO = "invalidRatio"
    MISSING_RATIO = "missingRatio"
    COLUMN_PROFILE = "columnProfile"
