import logging
import numpy as np
from sagemaker_data_insights.const import FeatureType as ft


def get_feature_type(metrics: dict, allowed_types: list = None, prefer_categorical=False) -> tuple:
    """
    Feature type analyzer

    Parameters
    ----------
    metrics : dict
        must include all the following keys: `median`, `numeric_finite_count`, `nrows`, `null_like_count`,
        `empty_count`, `whitespace_count`, `cardinality`, `datetime_count`, `datetime_non_float_count` and
        `datetime_rows_parsed`. Keys definitions can be found in const.py. While `x` is usually a sample of the data,
        the metrics should be calculated on the whole data or on a larger sample.
    allowed_types: list(str)
        List of allowed feature types. Can include the following types from const.py: NUMERIC, CATEGORICAL, TEXT,
        DATETIME, BINARY. By default includes all.
    prefer_categorical: bool
        Prefer categorical types to numerical types in case of ties.

        TODO. This flag is being used for Ganymede and will be tested for use as
        a default option in Data Insights. If it becomes a default option,
        consumers of data insights will need to do regression tests when they
        upgrade to the 2.0 branch (this branch).

    Returns
    -------
    str: feature type
        The type with the highest probability out of the types allowed in `allowed_types`
    dict: feature type probabilities
        The probability for the feature to be each of the types NUMERIC, CATEGORICAL, TEXT, DATETIME, BINARY. Type not
        included in `allowed_types` will have a zero probability
"""
    # TODO: add detection of ft.VECTOR copy logic from
    #  https://code.amazon.com/packages/AIAlgorithmsDataInsights/commits/081735f1f34b8c8ea7e24f76c390f84036f98e84

    # The order of all_types is used to break ties
    # the types are ordered by importance.
    if prefer_categorical:
        all_types = [ft.BINARY, ft.CATEGORICAL, ft.NUMERIC, ft.TEXT, ft.DATETIME]
    else:
        all_types = [ft.BINARY, ft.NUMERIC, ft.CATEGORICAL, ft.TEXT, ft.DATETIME]

    if not allowed_types:
        allowed_types = all_types
    else:
        for t in allowed_types:
            if t not in all_types:
                raise ValueError(f"Error: type {t} is not allowed. Allowed types: {allowed_types}")
    probs = _calculate_schema_probs(
        allowed_types,
        metrics["median"],
        metrics["numeric_finite_count"],
        metrics["nrows"],
        metrics["null_like_count"],
        metrics["empty_count"],
        metrics["whitespace_count"],
        metrics["cardinality"],
        metrics["datetime_count"],
        metrics["datetime_non_float_count"],
        metrics["datetime_rows_parsed"],
    )

    # We will use the column type with the highest score, breaking ties using
    # binary > numeric > categorical > text > datetime unless prefer_categorical is set, in which case we use
    # binary > categorical > numeric > text > datetime to break ties.
    score_type_pairs = [(probs[key], key) for key in all_types]
    score_type_pairs.sort(key=lambda x: -x[0])  # This sort is stable, so will preserve order above on ties
    _, col_type = score_type_pairs[0]
    logging.debug(f"col_type: {col_type}")
    return col_type, probs


def _calculate_schema_probs(  # noqa: C901
    allowed_types,
    median,
    numeric_finite_count,
    nrows,
    null_like_count,
    empty_count,
    whitespace_count,
    cardinality,
    datetime_count,
    datetime_non_float_count,
    datetime_rows_parsed,
) -> dict:
    """
    Calculates the probabilities for the feature to be any of the types of `schema_types` based on a set of heuristic
    rules

    Parameters
    ----------
    allowed_types: list(str)
        List of allowed feature types. Can include the following types from const.py: NUMERIC, CATEGORICAL, TEXT,
        DATETIME, BINARY. By default includes all.
    median: see description in `const.py`
    numeric_finite_count: see description in `const.py`
    nrows: see description in `const.py`
    null_like_count: see description in `const.py`
    empty_count: see description in `const.py`
    whitespace_count: see description in `const.py`
    cardinality: see description in `const.py`
    datetime_count: see description in `const.py`
    datetime_non_float_count: see description in `const.py`
    datetime_rows_parsed: see description in `const.py`

    Returns
    -------
    dict: feature type probabilities
        The probability for the feature to be each of the types NUMERIC, CATEGORICAL, TEXT, DATETIME, BINARY. Type not
        included in `allowed_types` will have a zero probability
"""
    # Initialize all types to zero
    numeric = 0
    categorical = 0
    text = 0
    datetime = 0
    binary = 0

    # Probability-like score of column being numeric is proportional to the fraction of entries castable to float.
    if ft.NUMERIC in allowed_types and not np.isnan(median):
        numeric = numeric_finite_count / (nrows - null_like_count - empty_count - whitespace_count)

    # Probability-like score of column being text is proportional to the fraction of non-numeric, non-empty entries.
    if ft.TEXT in allowed_types:
        text_like_rows = nrows - numeric_finite_count - null_like_count - empty_count - whitespace_count
        text = text_like_rows / nrows

    if cardinality == 2:
        if ft.BINARY in allowed_types:
            binary = 1.0
            text = 0.0
        if ft.CATEGORICAL in allowed_types:
            categorical = 1.0
            text = 0.0
    elif ft.CATEGORICAL in allowed_types:
        if cardinality / nrows < 0.01:
            # If there are on average more than 1/.01 = 100 entries per category, use full categorical and disable text.
            categorical = 1.0
            text = 0.0
        elif 0.01 <= cardinality / nrows < 0.2:
            # If there are on average fewer than 1/.01 = 100 but more than 1/.2 = 5 entries per category,
            # then proportionally decrease probability to zero.
            categorical = 1 - (cardinality / nrows - 0.01) / 0.19
        else:
            # Don't count as categorical if on average there are fewer than 5 entries per category.
            categorical = 0.0

    if (
        ft.DATETIME in allowed_types
        and datetime_non_float_count / datetime_rows_parsed > 0.05
        and datetime_count / datetime_rows_parsed > 0.6
    ):
        datetime = 1.0
        text = 0.0
        categorical = 0.0
        numeric = 0.0

    # Normalize so that scores sum to 1.
    normalizing_sum = numeric + categorical + text + datetime + binary
    if normalizing_sum == 0:
        raise ValueError(f"Error: scores for all allowed types are zero. Allowed types: {allowed_types}")
    numeric = numeric / normalizing_sum
    categorical = categorical / normalizing_sum
    text = text / normalizing_sum
    datetime = datetime / normalizing_sum
    binary = binary / normalizing_sum

    return {ft.NUMERIC: numeric, ft.CATEGORICAL: categorical, ft.TEXT: text, ft.DATETIME: datetime, ft.BINARY: binary}
