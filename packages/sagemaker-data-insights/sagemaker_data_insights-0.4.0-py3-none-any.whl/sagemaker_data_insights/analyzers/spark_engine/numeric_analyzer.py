from pyspark.sql import DataFrame
from sagemaker_data_insights.const import INSIGHTS


def analyze_numeric_feature(column: DataFrame, metrics: dict) -> dict:
    """
    Analyzes a numeric feature.

    column: pyspark.sql.DataFrame
    metrics: dict
    """

    generated_insights = []

    # TODO: Implement insights for numeric features

    return {
        INSIGHTS: generated_insights
    }
