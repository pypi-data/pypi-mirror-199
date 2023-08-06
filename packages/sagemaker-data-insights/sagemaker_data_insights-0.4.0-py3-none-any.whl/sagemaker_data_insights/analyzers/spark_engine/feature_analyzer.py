from pyspark.sql import DataFrame
from sagemaker_data_insights.const import DeequFeatureType as ft, INSIGHTS
from sagemaker_data_insights.analyzers.spark_engine.numeric_analyzer import analyze_numeric_feature
from sagemaker_data_insights.analyzers.spark_engine.string_analyzer import analyze_string_feature
from sagemaker_data_insights.analyzers.spark_engine.string_analyzer import analyze_text_feature
from sagemaker_data_insights.insights import Insights


def analyze_feature_column(column: DataFrame, feature_type: str, profiles, requested_insights=None) -> dict:
    """
    Analyze a feature column in a dataframe and generate feature insights

    Args:
        column: a dataframe with single column
        feature_type: str,
        profiles: dict, column profiles
        requested_insights: list, requested insights, if None generates all applicable insights
    """

    insights = {
        "type": feature_type,
        "metrics": profiles.all,
        "missing_ratio": 1 - profiles.completeness,
        "unique_count": profiles.approximateNumDistinctValues
    }

    # Common insights that are universal to all feature types
    common_insights = []

    if profiles.completeness < Insights.MISSING_VALUES_THRESHOLD:
        common_insights.append(Insights.generate(Insights.MISSING_VALUES, Insights.MEDIUM_FEATURE))

    if profiles.approximateNumDistinctValues == 1:
        common_insights.append(Insights.generate(Insights.CONSTANT_FEATURE, Insights.LOW))

    if profiles.approximateNumDistinctValues == len(column.columns):
        common_insights.append(Insights.generate(Insights.ID_COLUMN, Insights.LOW))

    # Generates insights for each feature type
    if feature_type != ft.UNKNOWN:
        insights.update(
            {
                ft.FRACTIONAL: lambda: analyze_numeric_feature(column, profiles),
                ft.INTEGRAL: lambda: analyze_numeric_feature(column, profiles),
                ft.STRING: lambda: analyze_string_feature(column, profiles),
                ft.TEXT: lambda: analyze_text_feature(column, profiles),
            }[feature_type]()
        )

    for i in common_insights:
        insights[INSIGHTS].append(i)

    return insights
