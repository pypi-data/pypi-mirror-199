import logging
import pandas as pd
import scipy.stats as sp

from sagemaker_data_insights import PEARSON, ALLOWED_CROSS_COL_INSIGHTS
from sagemaker_data_insights import FEATURE_TYPES, FEATURE_DATA
from sagemaker_data_insights import FeatureType as ft
from sagemaker_data_insights.model_utils import _encode_features


def cross_column_stats(
    left_feature_set: dict, right_feature_set: dict, requested_insights: list = None, n_jobs: int = 1
):
    """
    Computes various pairwise statistics between two sets of feature vectors.
    The following correlations are calculated:
    {PEARSON}: Pearson Correlation is a linear correlation measure between two features. It is in the range [-1,1],
        where 0 indicates that the features are independent and 1 (or -1) indicates that they are completely
        linearly dependent. It is to be noted that pearson correlation only captures only linear relationships.

    Parameters
    ----------
    left_feature_set: dict
        Represents the first set of feature vectors as
        {
            {FEATURE_DATA}: pandas.DataFrame
            {FEATURE_TYPES}: dict(str:str) - maps column names to column types
        }
        - Only {NUMERIC}, {BINARY} and {CATEGORICAL} types are supported.
        - Type Error is raised if the given feature type is not supported.

    right_feature_set: dict
        The second set of feature vectors, representation is same as left_feature_set.

    requested_insights: list(str)
        A list of the requested metrics to be returned.
        - If not provided, all the insights in {ALLOWED_CROSS_COL_INSIGHTS} is returned.

    n_jobs : int
        number of cores to use in feature processing

    Returns
    ----------

    dict: cross column insights
        The python dictionary maps each data insight key requested to the calculated data insights.

        - Each data insight is a matrix of correlation values between two feature pairs. This is represented as the
        following structure (returned by the pd.DataFrame.to_dict() function, with "split" orient):
        {
            "columns": List of feature names from [left_feature_set], representing the columns of the matrix
            "index": List feature names from [right_feature_set], representing the row index of the matrix
            "data": 2-D list of the correlation values, representing the correlation matrix
        }

        Example:
        Consider a correlation matrix calculated for a particular insight, between [left_1, left_2] columns in
        [left_feature_set] and [right_1, right_2] columns in [right_feature_set] shown below.

                left_1      left_2
        right_1    1.0         2.9
        right_2    3.9         1.2

        The correlation matrix would be represented as following in the response structure:
        {
            "columns": ["left_1", "left_2"]
            "index": ["right_1", "right_2"]
            "data": [[1.0, 2.9], [3.9, 1.2]]
        }
    """

    cross_column_insights = {}

    if requested_insights is None:
        requested_insights = ALLOWED_CROSS_COL_INSIGHTS

    # Encoding feature columns
    left_encoded = pd.DataFrame(
        _encode_features(
            left_feature_set[FEATURE_TYPES],
            left_feature_set[FEATURE_DATA],
            [ft.NUMERIC, ft.BINARY, ft.CATEGORICAL],
            False,
            n_jobs=n_jobs,
        )["transformed_data"],
        columns=left_feature_set[FEATURE_DATA].columns,
    )

    left_numeric_binary = [
        name for name, ftype in left_feature_set[FEATURE_TYPES].items() if ftype in [ft.NUMERIC, ft.BINARY]
    ]
    right_encoded = pd.DataFrame(
        _encode_features(
            right_feature_set[FEATURE_TYPES],
            right_feature_set[FEATURE_DATA],
            [ft.NUMERIC, ft.BINARY, ft.CATEGORICAL],
            False,
            n_jobs=n_jobs,
        )["transformed_data"],
        columns=right_feature_set[FEATURE_DATA].columns,
    )
    right_numeric_binary = [
        name for name, ftype in right_feature_set[FEATURE_TYPES].items() if ftype in [ft.NUMERIC, ft.BINARY]
    ]

    # Calculating correlation between numeric & binary features in the left feature array to the numeric & binary
    # features in the right feature array
    if PEARSON in requested_insights:
        if left_numeric_binary and right_numeric_binary:
            correlations_df = pd.DataFrame(columns=left_numeric_binary, index=right_numeric_binary)
            for col in left_numeric_binary:
                for index in right_numeric_binary:
                    correlations_df.at[index, col] = sp.pearsonr(left_encoded[col], right_encoded[index])[0]
            cross_column_insights[PEARSON] = correlations_df.to_dict("split")
        elif right_numeric_binary:
            logging.warning(
                "WARNING: %s correlation for numeric and binary features can not be calculated because the left "
                "feature set has no numeric or binary features.",
                PEARSON,
            )
        elif left_numeric_binary:
            logging.warning(
                "WARNING: %s correlation for numeric and binary features can not be calculated because the right "
                "feature set has no numeric or binary features.",
                PEARSON,
            )
        else:
            logging.warning(
                "WARNING: %s correlation for numeric and binary features can not be calculated because neither of the "
                "feature sets have numeric or binary features.",
                PEARSON,
            )
    return cross_column_insights
