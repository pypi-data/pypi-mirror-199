import pandas as pd
import scipy
from sagemaker_data_insights.insights import Insights
from sagemaker_data_insights.const import INSIGHTS, FeatureType as ft
from sagemaker_data_insights.utils.column_utils import valid_ratio, get_valid_transformed_data


def analyze_numeric_feature(x_transformed: pd.Series, metrics: dict, frequent_elements: dict) -> dict:
    """
    Feature analyzer for a numeric column
    Parameters
    ----------
    x_transformed: pd.Series
    metrics: dict, metrics for x_transformed
    frequent_elements: dict, frequenct elements calculated using histogram_functions.calc_frequent_elements

    Returns
        a dictionary of:
        skew: calculated using scipy.stats.skew
        kurtosis: calculated using scipy.stats.kurtosis
        valid_ratio*: ratio of the number of finite numeric values to the number of samples
        insights: pure statistical column insights
    -------

    """
    _, x_transformed_valid = get_valid_transformed_data(x_transformed)
    # Insights for numeric feature
    insights = []

    # TODO: factor out insights
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
        "skew": float(scipy.stats.skew(x_transformed_valid.ravel())),
        "kurtosis": float(scipy.stats.kurtosis(x_transformed_valid.ravel())),
        "valid_ratio": valid_ratio(metrics, ft.NUMERIC),
        INSIGHTS: insights
    }
