from sagemaker_data_insights.const import INSIGHTS, FeatureType as ft
from sagemaker_data_insights.utils.column_utils import valid_ratio


def analyze_binary_feature(metrics: dict) -> dict:
    """
    Binary column feature analyzer
    Parameters
    ----------
    metrics: dict, metrics of the column

    Returns
    -------
    valid_ratio: ratio of the number of not null like values and not whitespace strings to the number of
                samples
    """
    return {
        "valid_ratio": valid_ratio(metrics, ft.BINARY),
        INSIGHTS: [],
    }
