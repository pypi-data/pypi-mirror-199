import pandas as pd
import numpy as np

from sagemaker_data_insights.const import FeatureType as ft


def _numpy_conversion(x: pd.Series, y: pd.Series = None) -> tuple:
    """
    Converts original pandas column data to numpy and excludes null value.

    Parameters
    ----------
    x : pandas.Series
        raw column data
    y : pandas.Series or Nones
        raw target column data(if any)

    Returns
    -------
    x_numpy : np.ndarray
              Non-null x in numpy
    y_numpy : None or np.ndarray
              None if y is None, otherwise non-null y in numpy
    """
    x_numpy = x.to_numpy().reshape((-1, 1))
    valid_idxs = ~pd.isnull(x_numpy)
    x_numpy = x_numpy[valid_idxs].astype(str).reshape((-1, 1))
    y_numpy = None if y is None else y.to_numpy().reshape((-1, 1))[valid_idxs].reshape((-1, 1))
    return x_numpy, y_numpy


def missing_ratio(metrics: dict) -> float:
    return float((metrics["null_like_count"] + metrics["empty_count"] + metrics["whitespace_count"]) / metrics["nrows"])


def valid_ratio(metrics: dict, feature_type: str) -> float:
    if feature_type == ft.NUMERIC:
        return float(metrics["numeric_finite_count"] / metrics["nrows"])
    if feature_type in [ft.CATEGORICAL, ft.BINARY, ft.TEXT]:
        return float(
            (metrics["nrows"] - metrics["null_like_count"] - metrics["empty_count"] - metrics["whitespace_count"])
            / metrics["nrows"]
        )
    if feature_type == ft.DATETIME:
        return float(metrics["datetime_count"] / metrics["datetime_rows_parsed"])
    if feature_type == ft.VECTOR:
        return 1 - missing_ratio(metrics)
    raise ValueError(f"Unsupported feature type {feature_type}")


def get_valid_transformed_data(x_transformed: np.array):
    valid_idxs = np.isfinite(x_transformed)
    x_transformed_valid = x_transformed[valid_idxs]
    return valid_idxs, x_transformed_valid


def unique_without_whitespaces(x):
    """
    Returns the list of unique items with their counts excluding items of only whitespaces. Items of only whitespaces
    are considered missing thus they are not valid keys for frequent elements plots
    """
    unique, counts = np.unique(x, return_counts=True)
    unique_ = []
    counts_ = []
    for u, c in zip(unique, counts):
        if str(u).strip() != "":
            unique_.append(u)
            counts_.append(int(c))
    return np.array(unique_), np.array(counts_)
    
