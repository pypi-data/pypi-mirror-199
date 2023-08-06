import logging
import pandas as pd
from sagemaker_data_insights.column_data_insights.utils import _get_transformed_col_data

from sagemaker_data_insights.const import FeatureType as ft
from sagemaker_data_insights.analyze_feature import get_feature_type, missing_ratio, valid_ratio
from .constants import ColumnDataInsightsParamsKeys as CDP
from .utils import _calc_column_stats, _fetch_categorical_data, _fetch_non_categorical_data


def _get_column_profile(unique_count, feature_type: str, pandas_df_col: pd.Series) -> dict:
    """
    Get column profile data

        Args:
            unique_count: Number of unique items in the column
            feature_type: Logical data type [ft.NUMERIC, ft.DATETIME, ft.CATEGORICAL, ft.BINARY, ft.TEXT]
            pandas_df_col: Column pandas.Series

        Returns:
            data: JSON of either robust histogram data or categorical data
    """
    data = {}
    transformed_col_data = _get_transformed_col_data(feature_type, pandas_df_col)

    if feature_type in [ft.NUMERIC, ft.DATETIME]:
        data = _fetch_non_categorical_data(unique_count, transformed_col_data)
    elif feature_type in [ft.CATEGORICAL, ft.BINARY, ft.TEXT]:
        data = _fetch_categorical_data(unique_count, transformed_col_data)

    return data


def get_column_insights_data(col: str, pandas_df_col: pd.Series) -> tuple:
    """
    Get insights data for a single column

        Args:
            col: Column name
            pandas_df_col: Column pandas.Series

        Returns:
            res: JSON that includes column insights data
    """
    res = {
        CDP.COLUMN_NAME: col,
        CDP.LOGICAL_DATA_TYPE: None,
        CDP.VALID_RATIO: None,
        CDP.INVALID_RATIO: None,
        CDP.MISSING_RATIO: None,
        CDP.COLUMN_PROFILE: None,
    }
    try:
        stats = _calc_column_stats(pandas_df_col)
    except Exception as e:  # pylint: disable=W0703
        logging.error(f"Failed to calculate basic stats for column {col} - {e}")
        return res, {}

    try:
        feature_type, _ = get_feature_type(stats, prefer_categorical=True)
        res[CDP.LOGICAL_DATA_TYPE] = feature_type
    except Exception as e:  # pylint: disable=W0703
        logging.error(f"Failed to calculate feature type for column {col} - {e}")
        return res, {}

    # feature_type could be unknown
    if feature_type in [ft.NUMERIC, ft.DATETIME, ft.CATEGORICAL, ft.BINARY, ft.TEXT]:
        miss_r = missing_ratio(stats)
        valid_r = valid_ratio(stats, feature_type)
        invalid_r = 1 - valid_r - miss_r

        res[CDP.VALID_RATIO] = valid_r
        res[CDP.INVALID_RATIO] = invalid_r
        res[CDP.MISSING_RATIO] = miss_r

        try:
            unique_count = stats["cardinality"]
            column_profile = _get_column_profile(unique_count, feature_type, pandas_df_col)
            res[CDP.COLUMN_PROFILE] = column_profile
        except Exception as e:  # pylint: disable=W0703
            logging.error(f"Failed to calculate profile data for column {col} - {e}")
            return res, {}
    else:
        logging.error(f"The feature type {feature_type} is not accepted in column data insights")

    return res, {col: stats}
