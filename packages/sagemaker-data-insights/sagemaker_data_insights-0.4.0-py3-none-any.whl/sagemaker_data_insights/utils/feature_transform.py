import numpy as np
from sagemaker_data_insights.const import FeatureType as ft
from sagemaker_sklearn_extension.impute import RobustImputer
from sagemaker_data_insights.utils.date_time import DateTimeVectorizer


def get_feature_transform(feature_type: str, unknown_as_nan: bool):
    """
    Returns the default feature transform used by data_insights to do various tasks that require feature encoding
    including: quick model, anomaly detection, prediction power and more.
"""
    return {
        ft.NUMERIC: RobustImputer(strategy="constant", fill_values=np.nan) if unknown_as_nan else RobustImputer(),
        ft.DATETIME: DateTimeVectorizer(mode="ordinal"),
    }[feature_type]
