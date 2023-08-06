import pandas as pd
import logging
import sagemaker_data_insights.const as cs

from sagemaker_data_insights.const import FeatureType as ft
from sagemaker_data_insights.utils.column_utils import missing_ratio
from sagemaker_data_insights.analyzers.binary_analyzer import analyze_binary_feature
from sagemaker_data_insights.analyzers.categorical_analyzer import analyze_categorical_feature
from sagemaker_data_insights.analyzers.datetime_analyzer import analyze_datetime_feature
from sagemaker_data_insights.analyzers.numeric_analyzer import analyze_numeric_feature
from sagemaker_data_insights.analyzers.text_analyzer import analyze_text_feature
from sagemaker_data_insights.analyzers.vector_analyzer import analyze_vector_feature
from sagemaker_data_insights.utils.feature_transform import get_feature_transform
from sagemaker_data_insights.histogram_functions import calc_frequent_elements


def analyze_feature_column(x: pd.Series, feature_type: str, metrics: dict, requested_stats: list = None) -> dict:
    """
    Feature analyzer. Provides ML relevant statistics about the feature. Different statistics will be derived for each
    feature type.

    Parameters
    ----------
    x : pandas.Series
        raw feature column vector (e.g. NOT encoded using one hot encoder)
    feature_type: str
        NUMERIC, CATEGORICAL, TEXT, DATETIME or BINARY. If unknown, use `get_feature_type`
    metrics : dictionary that must include all the following keys: nrows, numeric_finite_count, cardinality and
        empty_count. See the descriptions in const.py
    requested_stats : list of strings or None
        Possible values:
            None - return the default set of stats
        Additional values are:
        'text_stats' which return the default set of stats and the additionaly requested stats.
        For example: ['text_stats']

    Returns
    -------
    dict: data insights metrics. Statistics will be derived according to the provided feature type. The fields with *
    are derived from the provided metrics, all other - from x and y
        All feature types:
            name: feature name taken from x
            type: feature type provided in the input
            metrics*: metrics dict provided in the input
            prediction_power and normalized_prediction_power: available when y and task are provided
            frequent_elements: calculated using histogram_functions.calc_frequent_elements
            missing_ratio*: ratio of number of null like and empty rows to the number of rows
            {cs.INSIGHTS}: list of insights. Can include: TARGET_LEAKAGE, UNINFORMATIVE_FEATURE,
                NUMERIC_DISGUISED_MISSING_VALUE, CATEGORICAL_RARE_CATEGORIES
        Numeric:
            outliers_ratio: ratio of the number of outliers to number of samples
            skew: calculated using scipy.stats.skew
            kurtosis: calculated using scipy.stats.kurtosis
            valid_ratio*: ratio of the number of finite numeric values to the number of samples
        Categorical / Binary:
            valid_ratio*: ratio of the number of not null like values and not whitespace strings to the number of
                samples
        Text:
            valid_ratio*: ratio of the number of not null like values and not whitespace strings to the number of
                samples
            important_words: for each word prediction_power, normalized_prediction_power and frequency
            character_statistics: dictionary with character statistics. For each statistic a dictionary with
            frequent_elements. The possible character statistics are:
                    word_count: number of words
                    char_count: string length
                    special_ratio: ratio of non alphanumeric characters to non-spaces in the string, 0 if empty string
                    digit_ratio: ratio of digits characters to non-spaces in the string, 0 if empty string
                    lower_ratio: ratio of lowercase characters to non-spaces in the string, 0 if empty string
                    capital_ratio: ratio of uppercase characters to non-spaces in the string, 0 if empty string
                Note that some of them could be missing if there's only one value. For example, word_count will be
                missing if all texts contain exactly one word.
        Datetime:
            valid_ratio: ratio of number valid datetime values to the number of samples
            datetime_features: dict. Prediction power and robust histogram or frequent elements stats for each of the
                following: "month", "hour", "weekday", "year", "minute", "second", "week". Note that some items could
                be missing if there is no relevant data in the feature
    """
    if feature_type not in [ft.NUMERIC, ft.CATEGORICAL, ft.TEXT, ft.DATETIME, ft.BINARY, ft.VECTOR]:
        raise ValueError(
            f"feature_type must be one of {ft.NUMERIC}, {ft.CATEGORICAL}, {ft.TEXT}, {ft.DATETIME}, {ft.BINARY} or "
            f"{ft.VECTOR}"
        )

    x_numpy = x.to_numpy().reshape((-1, 1))
    valid_idxs = ~pd.isnull(x_numpy)
    x_numpy = x_numpy[valid_idxs].astype(str).reshape((-1, 1))

    insights = {
        "name": x.name,
        "type": feature_type,
        "metrics": metrics,
    }
    if len(x_numpy) == 0:
        insights["missing_ratio"] = 1
        insights["valid_ratio"] = 0
        insights["frequent_elements"] = []
        insights[cs.INSIGHTS] = []
        return insights

    if feature_type in [ft.NUMERIC, ft.DATETIME]:
        feature_transform = get_feature_transform(feature_type, True).fit(x_numpy)
        x_transformed = feature_transform.transform(x_numpy)

    insights["missing_ratio"] = missing_ratio(metrics)
    insights["frequent_elements"] = calc_frequent_elements(x_numpy)

    # Add insights and statistics specific for each feature type
    insights.update(
        {
            ft.NUMERIC: lambda: analyze_numeric_feature(
                x_transformed, metrics, insights["frequent_elements"]
            ),
            ft.TEXT: lambda: analyze_text_feature(
                x_numpy, metrics,  requested_stats=requested_stats
            ),
            ft.DATETIME: lambda: analyze_datetime_feature(
                feature_transform, x_transformed,  metrics
            ),
            ft.BINARY: lambda: analyze_binary_feature(metrics),
            ft.CATEGORICAL: lambda: analyze_categorical_feature(insights["frequent_elements"], metrics),
            ft.VECTOR: lambda: analyze_vector_feature(metrics),
        }[feature_type]()
    )

    return insights
