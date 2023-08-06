from sagemaker_data_insights.const import INSIGHTS, FeatureType as ft
from sagemaker_data_insights.utils.column_utils import valid_ratio


def analyze_vector_feature(metrics) -> dict:
    """
    Vector column feature analyzer
    Parameters
    ----------
    metrics: dict, metrics of the vector column

    Returns
    -------
    valid_ratio:  ratio of number of valid vector values to the number of samples

    """
    return {
        "valid_ratio": valid_ratio(metrics, ft.VECTOR),
        INSIGHTS: [],
    }
