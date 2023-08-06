import numpy as np
import pandas as pd
from sagemaker_data_insights.const import INSIGHTS, FeatureType as ft
from sagemaker_data_insights.utils.column_utils import valid_ratio
from sagemaker_data_insights.insights import Insights
from sagemaker_data_insights.text_utils import CharacterStatistics, token_importance
from sagemaker_data_insights.text_utils import sanitize_strings
from sagemaker_data_insights.patterns.analyze_patterns import analyze_text_patterns
from sagemaker_data_insights.histogram_functions import calc_frequent_elements


# TODO: add response payload so that the histograms can be computed
def analyze_text_feature(  # noqa: C901
        x: np.array,
        metrics: dict,
        random_state: int = 0,
        num_top_words: int = 200,
        requested_stats: list = None,
) -> dict:
    """
    Derive statistics and insights specific to text features.

    Parameters
    ----------
    x : np.ndarray of size (height, 1)
        text feature
    metrics : dictionary
        See the documentation in `analyze_feature`
    random_state: int
        random seed used for RNG
    num_top_words: int
        max number of most important words to return, see `from important_words` below
    requested_stats : list of strings or None
        Possible values:
            * 'text_stats' for statistics on the distrbution of characters and tokens
            * 'text_patterns' for results of an analysis of textual patterns

    Returns
    -------
    dict: text feature insights. See feature_analyzer.py
"""
    x_list = list(x.ravel())
    insights = {
        "valid_ratio": valid_ratio(metrics, ft.TEXT),
        INSIGHTS: [],
        "character_statistics": {},
    }

    if not requested_stats:
        return insights

    if "text_stats" in requested_stats:
        # Numeric character statistics: from every string extract various ratio and count statistics. These are numeric
        # features that capture various characteristics of the string
        for desc, func in CharacterStatistics.functions.items():
            feat = np.vectorize(func)(x_list).reshape((-1, 1))
            num_unique = len(np.unique(feat))
            if num_unique <= 1:
                continue
            feat_stats = {}
            feat_stats["frequent_elements"] = calc_frequent_elements(
                feat, y=None, task=None, max_num_elements=20, sort_type="value"
            )
            insights["character_statistics"][desc] = feat_stats

        # token importance: add information about token importance when tokenizing based on words
        insights["important_words"] = token_importance(
            x, y=None, task=None, analyzer="word", num_top_features=num_top_words
        )

    if "text_patterns" in requested_stats:
        expression_set = analyze_text_patterns(x.reshape(-1), min_coverage=0.8, random_state=random_state)
        num_experiments, sample_size = expression_set.experiment_statistics()

        pattern_columns = ["Pattern", "Relevance", "Regular expression", "Matches", "Non-matches"]
        pattern_dict = {k: [] for k in pattern_columns}

        for expr in expression_set.ranked_expressions():
            pattern = expr.annotated_str()
            confidence = expr.coverage_accumulator.value()

            # Surround matches and nonmatches with angle brackets to show whitespace.
            matches = sanitize_strings(expr.matches_histogram.top_n(5))
            nonmatches = sanitize_strings(expr.outliers_histogram.top_n(5))

            num_rows = max(len(matches), len(nonmatches))
            padding = [""] * (num_rows - 1)

            pattern_dict["Pattern"].extend([pattern] + padding)
            # Our external language for accuracy/confidence is 'Relevance'.
            pattern_dict["Relevance"].extend(["{:.2f}".format(100 * confidence)] + padding)
            pattern_dict["Regular expression"].extend([expr.regex(use_token_lengths=True)] + padding)
            pattern_dict["Matches"].extend(matches + [""] * (num_rows - len(matches)))
            pattern_dict["Non-matches"].extend(nonmatches + [""] * (num_rows - len(nonmatches)))

            # Getting insights
            if 1 > confidence >= Insights.HIGH_CONFIDENCE_PATTERN_THRESHOLD:
                insights[INSIGHTS].append(
                    Insights.generate(
                        Insights.HIGH_CONFIDENCE_PATTERN,
                        Insights.MEDIUM,
                        {
                            "pattern": pattern,
                            "confidence": confidence,
                            "num_experiments": num_experiments,
                            "sample_size": sample_size,
                        },
                    )
                )

        # If there are no patterns, return a table with a single column and an informative message.
        if expression_set.best_expression() is None:
            pattern_columns = ["Pattern"]
            pattern_dict = {"Pattern": ["No textual patterns found."]}

        pattern_df = pd.DataFrame(columns=pattern_columns, data=pattern_dict)
        insights["text_patterns"] = pattern_df.to_dict()

    return insights
