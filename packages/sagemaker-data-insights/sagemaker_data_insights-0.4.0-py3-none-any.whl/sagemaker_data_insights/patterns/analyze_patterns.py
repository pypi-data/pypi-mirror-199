from typing import List
import numpy as np

from .tokens import Tokens
from .expression import Expression, ExpressionSet, ExpressionSetType
from .parse import Parse


def analyze_text_patterns(
    strs: List[str],
    min_coverage: int = 0.8,
    sampling_iterations: int = 10,
    sampling_size: int = 30,
    max_tokens: int = 100,
    min_examples: int = 2,
    random_state: int = 0,
) -> ExpressionSetType:
    """Analyze strings and extract patterns.

    A list of strings (potentially large) is sampled and resampled. Each time
    the sample strings are parsed into expressions, and the expressions are
    tested for coverage accuracy against the sample, and the sample is used to
    record token length statistics. After a number of iterations, a set of
    candidate expressions is returned.

    The default values for the parameters have been tested on live and synthetic
    data sets. They balance performance and accuracy and shouldn't need to be
    adjusted.

    Args:
        strs (List[str]): a list of strings to analyze
        min_coverage (float, optional): The cut-off of minimum coverage of the expressions to return.
        sampling_iterations (int, optional): The number of samples to take in order to find patterns and statistics.
        sampling_size (int, optional): The sample size of strings to take when heuristically computing patterns and
                                       statistics. If there are fewer strings than this size, the entire set of strings
                                       will be used.
        max_tokens (int, optional): The maximum number of tokens allowed to parse in a string. Strings with more tokens
                                    are filtered out.
        min_examples (int, optional): Samples are filtered for suitable strings. This is the minimum size of a filtered
                                      sample to analyze.
        random_state (int, optional): A random state to seed the random number generator.

    Returns:
        ExpressionSetType: An expression set containing extracted (pattern)
        expressions and recorded statistics such as token length statistics or
        coverage statistics.  """
    # The perferred method for seeding a random number generator. See NEP 19
    # https://numpy.org/neps/nep-0019-rng-policy.html
    rng = np.random.default_rng(random_state)

    # In the event we don't have many strings, we can optimize the experiment.
    if len(strs) <= sampling_size:
        sampling_size = len(strs)
        sampling_iterations = 1

    expression_set = ExpressionSet(min_coverage=min_coverage)
    for _ in range(sampling_iterations):
        sample = rng.choice(strs, sampling_size, replace=False)

        # Remove strings with too many tokens.
        sample = list(filter(lambda x: len(Tokens.split_by_delimiters(x)) <= max_tokens, sample))

        # Ensure we have enough strings after filtering for long strings.
        if len(sample) < min_examples:
            continue

        # Parse the set of strings into pattern expressions.
        token_lists = [Parse.parse(s) for s in sample]
        exprs = [Expression(t) for t in token_lists]

        # Use the sample to calculate approximations to the coverage and token
        # length statistics.
        for expr in exprs:
            expr.coverage(sample)

        # Combine the new expressions into the expression set, aggregating any new statistics.
        expression_set.combine(exprs)
        expression_set.record_experiment(len(sample))

    return expression_set
