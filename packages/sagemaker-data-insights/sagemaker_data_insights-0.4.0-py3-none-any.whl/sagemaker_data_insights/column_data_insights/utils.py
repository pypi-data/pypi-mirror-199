import pandas as pd
import numpy as np
from sagemaker_data_insights.const import FeatureType as ft
from sagemaker_data_insights.analyze_feature import (
    get_feature_transform_and_transformed_x,
    get_valid_transformed_data,
    _numpy_conversion,
)

from sagemaker_data_insights.calc_stats_pandas_series import _calc_stats_pandas_series
from sagemaker_data_insights.histogram_functions import (
    _frequent_element_helper,
    calc_robust_histogram,
)

from .constants import (
    COUNT,
    DATA,
    VALUE,
    HistogramParamsKeys as HP,
    CategoricalParamsKeys as CP,
)


def _calc_column_stats(pandas_df_col: pd.Series, datetime_num_rows: int = 10000):
    """
    Calculate the basic statistics used by embedded data insights chart for a single pandas.Series

        Args:
            pandas_df_col: Column pandas.Series
            datetime_num_rows(Optional): Baseline for datetime type

        Returns:
            JSON of calculated stats
    """
    return _calc_stats_pandas_series(pandas_df_col, datetime_num_rows=datetime_num_rows, dw_light_mode=True)


def _cal_num_bins(count) -> int:
    """
    Calculate num of bins that will be shown in embedded data insights chart for non-categotical data

        Args:
            count: Number of unique items in the column

        Returns:
            num_of_bins(int)
    """
    return min(count, HP.HIST_MAX_BIN_NUM)


def _categorical_data_conversion(categorical_data, total_count, unique_count) -> dict:
    """
    Convert categorical data to expected form used by embedded data insights chart

        Args:
            categorical_data: categorical data result from _calc_categorical_elements func
            total_count: Number of total valid items in the column
            unqiue_count: Number of unique items in the column

        Returns:
            JSON of reformed categorical data
    """
    value_list = categorical_data[VALUE]
    count_list = categorical_data[COUNT]

    converted_categorical_data = []
    n = len(count_list)

    # categorical_data could be empty
    if n > 0:
        # Each element in categotical_data contains value and count
        # Value refers to the category name, count refers to the count for that category
        converted_categorical_data = [None] * (n + 1)
        for i in range(n):
            converted_categorical_data[i] = {VALUE: value_list[i], COUNT: count_list[i]}

        # FIXME: If there is a value in the data same as `CP.OTHER`, we can't distinguish between that and the one below
        # Construct "Other" category for rest categories
        converted_categorical_data[i + 1] = {VALUE: CP.OTHER, COUNT: total_count - sum(count_list)}

    return {CP.DISTINCT_VALUES: unique_count, DATA: converted_categorical_data}


def _non_categorical_data_conversion(robust_histogram_data) -> dict:
    """
    Convert histogram data to expected form used by embedded data insights chart

        Args:
            robust_histogram_data: results from sagemaker-data-insights lib's robust_histogram_data func

        Returns:
            JSON of reformed robust non-categorical data
    """
    # count_list and edges_list are returned from calc_robust_histogram func
    # https://github.com/aws/sagemaker-data-insights/blob/main/src/sagemaker_data_insights/histogram_functions.py#L9
    # It calls np.histogram under the hood. According to the doc
    # (https://numpy.org/doc/stable/reference/generated/numpy.histogram.html)
    # it is guaranteed that bin_edges will be(length(hist)+1)
    count_list = robust_histogram_data[HP.HIST_COUNT]
    edges_list = robust_histogram_data[HP.HIST_EDGES]
    lower_is_outlier = robust_histogram_data[HP.LOWER_BIN_IS_OUTLIER]
    upper_is_outlier = robust_histogram_data[HP.UPPER_BIN_IS_OUTLIER]

    converted_histogram_data = []
    n = len(count_list)

    # The valid_num_of_bins comes from calc_robust_histogram func
    # (https://github.com/aws/sagemaker-data-insights/blob/main/src/sagemaker_data_insights/histogram_functions.py#L9)
    # It shall be handled in calc_robust_histogram, add double check here just in case
    valid_num_of_bins = 3
    if n >= valid_num_of_bins:
        # The edges tuple is 1-1 mapping to count
        # Each edge tuple contains two values: MIN and MAX, which are used to construct bin boundaries
        edges_tuple_list = [None] * n
        for i in range(n):
            edges_tuple_list[i] = (edges_list[i], edges_list[i + 1])

        converted_histogram_data = [None] * n
        for i in range(n):
            if i == 0:
                isOutlier = lower_is_outlier
            elif i == n - 1:
                isOutlier = upper_is_outlier
            else:
                isOutlier = False
            converted_histogram_data[i] = {
                HP.MIN_VALUE: edges_tuple_list[i][0],
                HP.MAX_VALUE: edges_tuple_list[i][1],
                COUNT: count_list[i],
                HP.IS_OUTLIER: isOutlier,
            }

    return {DATA: converted_histogram_data}


def _get_transformed_col_data(feature_type: str, pandas_df_col: pd.Series) -> list:
    """
    Get transforemd column data based on feature types used by embedded data insights column profile calculation

        Args:
            feature_type: feature type of the column
            pandas_df_col: origin pandas dataframe column
        Returns:
            res: transformed column data
    """
    res = []
    if feature_type == ft.NUMERIC:
        pandas_df_col_numpy, _ = _numpy_conversion(pandas_df_col, None)
        _, pandas_df_col_transformed = get_feature_transform_and_transformed_x(feature_type, pandas_df_col_numpy)
        _, _, pandas_df_col_transformed_valid = get_valid_transformed_data(pandas_df_col_transformed, None)
        res = pandas_df_col_transformed_valid.ravel()
    elif feature_type == ft.DATETIME:
        # Datetime is converted to numeric for histogram calculation
        # [TODO]: Check if there is a better way for datetime conversion
        # transform column data
        datetime_col = pd.to_datetime(pandas_df_col.astype(str), errors="coerce", utc=True)
        res = pd.to_numeric(datetime_col)
    elif feature_type in [ft.CATEGORICAL, ft.BINARY, ft.TEXT]:
        pandas_df_col_numpy, _ = _numpy_conversion(pandas_df_col, None)
        res = pandas_df_col_numpy
    return res


def _fetch_non_categorical_data(unique_count, data) -> dict:
    """
    Fetch non-categorical data used by embedded data insights column profile calculation

        Args:
            unique_count: total count of unique items in the column
            data: transformed column data
        Returns:
            converted non-categotical data in the form used by embedded data insights column profile
    """
    num_bins = _cal_num_bins(unique_count)
    robust_histogram_data = calc_robust_histogram(data, num_bins=num_bins)
    return _non_categorical_data_conversion(robust_histogram_data)


def _fetch_categorical_data(unique_count, data) -> dict:
    """
    Fetch categorical data used by embedded data insights column profile calculation

        Args:
            unique_count: total count of unique items in the column
            data: transformed column data
        Returns:
            converted categotical data in the form used by embedded data insights column profile
    """
    categorical_data, total_count = _calc_categorical_elements(data)
    return _categorical_data_conversion(categorical_data, total_count, unique_count)


def _calc_categorical_elements(pandas_df_col: np.ndarray, max_num_elements=10) -> tuple:
    """
    Calculate categorical elements that will be shown in embedded data insights chart for categorical data

        Args:
            pandas_df_col: Column pandas.Series
            max_num_elements(Optional): Top x most frequent elements

        Returns:
            categorical_data_dict: Dict that contains categorical value and its count
            total_count: Number of valid items in the column
    """
    _, _, unique, counts, num_values, indices = _frequent_element_helper(pandas_df_col, None, max_num_elements)
    f = {"value": unique[indices].tolist(), "count": counts[indices].tolist()}
    return f, int(num_values)
