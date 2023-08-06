from pyspark.sql import DataFrame
from sagemaker_data_insights.const import INSIGHTS


def analyze_string_feature(column: DataFrame, metrics: dict) -> dict:
    """
    Analyzes a numeric feature.

    column: pyspark.sql.DataFrame
    metrics: dict, column profiles
    """

    generated_insights = []

    # TODO: Implement insights for string features

    return {
        INSIGHTS: generated_insights
    }


def analyze_text_feature(column: DataFrame, metrics: dict) -> dict:
    """
    Analyzes a text feature.

    column: pyspark.sql.DataFrame
    metrics: dict, column profiles
    """

    generated_insights = []

    # TODO: Implement insights for text features

    return {
        INSIGHTS: generated_insights
    }
