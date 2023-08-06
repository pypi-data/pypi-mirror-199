import numpy as np
from sagemaker_data_insights.utils.column_utils import valid_ratio
from sagemaker_data_insights.const import INSIGHTS, FeatureType as ft
from sagemaker_data_insights.histogram_functions import calc_frequent_elements, calc_robust_histogram


def analyze_datetime_feature(
    feature_transform, x_transformed: np.array, metrics: dict
) -> dict:
    """
    Date time analyzer
    Parameters
    ----------
    feature_transform
    x_transformed
    metrics: dict, metrics for datetime column

    Returns
    -------
    dict:
        valid_ratio
        datetime_features
        insights: list of insights
    """
    datetime_features = {}
    num_bins = 20
    # go over the internal features produced by the feature_transform e.g. week, month, hour etc.
    for idx, e in enumerate(feature_transform.extract_):
        col = x_transformed[:, idx].reshape((-1, 1))
        valid_rows = np.isfinite(col)
        col = col[valid_rows].reshape((-1, 1))

        internal_feature_insights = {}
        # All the datetime properties start with "extract_", e.g "extract_week", "extract_month"
        if e.extract_func.__name__[:8] != "extract_":
            raise ValueError("Not a valid datetime feature")
        internal_feature_name = e.extract_func.__name__[8:]  # remove `extract_` from the head of the string

        # Some internal feature types should always be frequent elements. For others, they are frequent elements when
        # they contain few unique elements or histogram when they contain many unique elements
        if internal_feature_name in ["quarter", "month", "hour", "weekday"] or len(np.unique(col)) <= num_bins:
            internal_feature_insights["frequent_elements"] = calc_frequent_elements(
                col.astype(int), None, task=None, sort_type="value", max_num_elements=len(np.unique(col))
            )
        else:
            internal_feature_insights["robust_histogram"] = calc_robust_histogram(
                col, None, task=None, num_bins=num_bins
            )
        datetime_features[internal_feature_name] = internal_feature_insights

    return {
        "valid_ratio": valid_ratio(metrics, ft.DATETIME),
        "datetime_features": datetime_features,
        INSIGHTS: [],
    }
