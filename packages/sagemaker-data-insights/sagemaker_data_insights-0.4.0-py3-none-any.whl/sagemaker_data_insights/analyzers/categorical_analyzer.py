import numpy as np
from sagemaker_data_insights.const import INSIGHTS, FeatureType as ft
from sagemaker_data_insights.insights import Insights
from sagemaker_data_insights.utils.column_utils import valid_ratio


def analyze_categorical_feature(frequent_elements: dict, metrics: dict) -> dict:
    """
    Categorical feature analyzer
    Parameters
    ----------
    frequent_elements: dict frequent elements produced by histogram_functions._calc_frequent_elements
    metrics: dict column metrics for feature column

    Returns
    -------
        valid_ratio: ratio of the number of not null like values and not whitespace strings to the number of
                samples
        insights: dict
    """
    insights = []
    if not frequent_elements["frequency"]:  # The column contains only missing values
        return {"valid_ratio": 0, INSIGHTS: insights}
    normalized_frequency = np.array(frequent_elements["frequency"]) / frequent_elements["frequency"][0]
    num_rare_categories = sum(normalized_frequency < Insights.CATEGORICAL_RARE_CATEGORIES_THRESHOLD)
    if num_rare_categories > Insights.NUM_RARE_CATEGORIES_THRESHOLD:
        rare_categories = list(np.array(frequent_elements["value"])[normalized_frequency <
                                                                    Insights.CATEGORICAL_RARE_CATEGORIES_THRESHOLD])
        rare_categories_frequency = list(np.array(frequent_elements["frequency"])[normalized_frequency < Insights.CATEGORICAL_RARE_CATEGORIES_THRESHOLD])
        insights.append(
            Insights.generate(
                Insights.CATEGORICAL_RARE_CATEGORIES,
                Insights.MEDIUM_FEATURE,
                {"rare_categories": rare_categories, "rare_categories_frequency": rare_categories_frequency},
            )
        )
    return {
        "valid_ratio": valid_ratio(metrics, ft.CATEGORICAL),
        INSIGHTS: insights,
    }
