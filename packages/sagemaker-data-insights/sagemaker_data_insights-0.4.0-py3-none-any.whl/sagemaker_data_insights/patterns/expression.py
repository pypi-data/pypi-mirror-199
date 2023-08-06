import re
import sys
from typing import Iterator, List, Set, Type, Union

import numpy as np

from .tokens import Tokens, TokenType
from .utils import AverageAccumulator, Histogram


class Expression:
    # TODO. Pattern learning doesn't create expressions with consecutive
    # semantic tokens, but Expressions can in theory have them.  Not all the
    # methods e.g. record_statistics play well when there are consec. semantic
    # tokens. Eliminate the possibility, by checking in initialization.
    """
    An expression is a well-formed formula in the grammar below, that
    additionally holds statistical information such as the witnessed token
    lengths, coverage data, and the "specificity" of the expression.

        Expression := Token | Token Expression
        Token := SemanticType | Delimiter
        SemanticType := {title} |
                 {upper} |
                 {lower} |
                 {alphanum} |
                 {digits} |
                 {mixed} |
                 {name}
                 ... (more types in future)
        Delimiter := , | ; | - | _ | @ | ...
        {alphanum} := [A-Za-z0-9]+
        {digits} := [0-9]+
        and so on.
        See Tokens class for more details.
        """

    def __init__(self, token_list):
        """Initializer for an Expression.

        Args:
            token_list (List of Token): A list of tokens that the expression will consist of.
        """
        self.token_list = token_list[:]
        self.token_length_histogram = [Histogram() for _ in token_list]
        self.specificity = self._specificity()
        self.coverage_accumulator = AverageAccumulator()
        # Keep track of seen outliers and matches so we can display them to the user.
        self.matches_histogram = Histogram()
        self.outliers_histogram = Histogram()

    def _specificity(self) -> float:
        """Calculates the specificity for this expression and stores it in the
        expression.

        Specificity is a heuristic to measure how specific the expression is on
        a scale from 0 to 10 with 0 being the least specific.  Each Token has a
        defined specificity with more specific tokens having a higher
        specificity. The specificity of an expression is defined as the average
        of the specificities of its tokens.

        Returns:
            The computed specificity.

        """
        if not self.token_list:
            return 10.0  # An empty string is a literal so it receives the highest specificity.

        return np.mean([s.specificity for s in self.token_list])

    def __ge__(self, other) -> bool:
        """Expressions are ranked by coverage and then specificity."""
        if self.coverage_accumulator.value() > other.coverage_accumulator.value():
            return True
        if (
            self.coverage_accumulator.value() == other.coverage_accumulator.value()
            and self.specificity >= other.specificity
        ):
            return True
        return False

    def __gt__(self, other) -> bool:
        """Expressions are ranked by coverage and then specificity."""
        if self.coverage_accumulator.value() > other.coverage_accumulator.value():
            return True
        if (
            self.coverage_accumulator.value() == other.coverage_accumulator.value()
            and self.specificity > other.specificity
        ):
            return True
        return False

    def regex(self, use_token_lengths: bool = False) -> str:
        """Produces the regular expression for this pattern.

        The regular expression will make use of the recorded token lengths to
        enforce token boundaries depending on whether use_token_lengths is true.

        Args:
            use_token_lengths (bool, optional): Whether or not to use
            witnessed token length statistics to for length specifiers in the
            regex. Defaults to False.

        Returns:
            string: the regular expression for this expression.
        """
        if use_token_lengths:
            regexes = [
                p.regex(length_specifier=Expression._length_range(h))
                for p, h in zip(self.token_list, self.token_length_histogram)
            ]
        else:
            regexes = [p.regex() for p in self.token_list]
        return "".join(regexes)

    def covers(self, s: str, use_token_lengths: bool = False, use_regex: bool = True) -> bool:
        """Whether or not this expression covers (matches) a string.

        Args:
            s (str): a string

            use_token_lengths (bool, optional): Whether or not to use
            witnessed token lengths for length specifiers. The string will not
            match if it has tokens of unwitnessed lengths. Defaults to False.

            use_regex (bool, optional): This option will be the default.

        Returns:
            bool: Whether or not the expression covers the string.
        """
        if use_regex:
            regex = self.regex(use_token_lengths=use_token_lengths)
            if re.fullmatch(regex, s):
                return True
            return False

        # The code below will be deprecated after performance benchmarks indicate that the
        # use regexes or compiled regexes is faster. The code will not detect {any}.
        # Beginning of legacy code.
        tokens = Tokens.split_by_delimiters(s)

        # There potentially are false negatives from this overly simplistic logic.
        if len(tokens) != len(self.token_list):
            return False

        if use_token_lengths:
            for token, pattern, hist in zip(tokens, self.token_list, self.token_length_histogram):
                length_range = Expression._length_range(hist)
                if not pattern.match(token, length_range=length_range):
                    return False

        else:
            for token, pattern in zip(tokens, self.token_list):
                if not pattern.match(token):
                    return False
        # End of legacy code.

        return True

    def _record_statistics(self, strs: List[str], matches: List[str]) -> None:
        """Records the statistics (e.g. token lengths) from a list of strings.

        If the expression does not cover the string, then no token length statistics are recorded.

        Args:
            strs (List(str)): A list of strings
            matches (List(str)): the subset of strs that this expression matches.
        """
        assert set(matches).issubset(set(strs))
        for s in strs:
            if s not in matches:
                self.outliers_histogram.witness(s)
                continue

            self.matches_histogram.witness(s)

            tokens = Tokens.split_by_delimiters(s)
            num_tokens = len(tokens)

            t = 0
            # The following loop will record witnessed word lengths into the
            # token length histogram for this expression.
            #
            # To do this, we align this expression's tokens with the words of
            # the string and record the lengths that we find in our length
            # statistics histogram.
            #
            # Some tokens can match empty strings. In an arbitrary setting this
            # can be ambiguous as there may be multiple alignments. But in our
            # language it is not ambiguous and we can proceed in a greedy
            # fashion.  This is because we cannot have consecutive semantic
            # tokens so we know if we don't match the next word (after we split
            # by delimiters), then we actually matched an empty string.
            for token, histogram in zip(self.token_list, self.token_length_histogram):
                # This is the case that the current token of this expression
                # matches the current token in the string. Note if t >=
                # num_tokens, the rest of the tokens in str must be empty
                # strings.
                if t < num_tokens and token.match(tokens[t]):
                    histogram.witness(len(tokens[t]))
                    t += 1
                # This is the case where we match an empty string. Thus we do
                # not increase the counter for which word we are on.
                else:
                    histogram.witness(0)

    def split_pos_neg(self, strs: List[str], use_token_lengths: bool = True) -> float:
        """Splits a set of strings into positive and negative examples for this expression.

        The positive examples are those which this expression covers/matches, and the
        negative examples are those which this expression does not cover/match.

        Args:
            strs (List of str): A list of strings
            token_lengths (bool, optional): Whether or not to use token length information in matching the
                strings.

        Returns:
            A pair of positive and negative lists of strings.
        """
        # Note simple benchmark using a loop vs two filters on N (large) items:
        # loop:  0.0009401636123657226
        # filter:  0.0011433355808258057
        # ratio:  1.2161027780567297 (using a filter is 1.21x the time)
        # Also, https://stackoverflow.com/questions/4578590/\
        # python-equivalent-of-filter-getting-two-output-lists-i-e-partition-of-a-list

        pos = [s for s in strs if self.covers(s, use_token_lengths=use_token_lengths)]
        neg = [x for x in strs if x not in pos]

        return pos, neg

    def f1_score(self, pos: List[str], neg: List[str], use_token_lengths: bool = False) -> float:
        """Calculate the F1-Score given a positive and negative set of examples for this expression.
        Division by 0 is avoided with sensible defaults. Recall is taken to be
        1.0 when there are no true positives, and precision is taken to be 1.0
        when there are no positive examples (TPs union FPs).
        If the precision and recall combine to 0, the F1 score is taken to be 0.

        Args:
            pos: A set of (true) positive strings.
            neg: A set of (true) negative strings.
            use_token_lengths (bool, optional): Whether or not to consider the token lengths when calculating
                coverage.

        Returns:
            3-tuple of float: The F1-Score, precision, and recall.
        """
        # Note: If pos is empty, coverage returns 1.0.
        recall = self.coverage(pos, record=False, use_token_lengths=use_token_lengths)

        true_pos = recall * len(pos)
        false_pos = self.coverage(neg, record=False, use_token_lengths=use_token_lengths) * len(neg)

        if abs(true_pos + false_pos) < sys.float_info.epsilon:
            precision = 1.0
        else:
            precision = true_pos / (true_pos + false_pos)

        if abs(precision + recall) < sys.float_info.epsilon:
            f1_score = 0.0
        else:
            f1_score = 2 * precision * recall / (precision + recall)

        return f1_score, precision, recall

    def coverage(self, strs: List[str], record: bool = True, use_token_lengths: bool = False) -> float:
        """Calculates the coverage on a set of strings.

        Args:
            strs (list(str)): A list of strings
            record (bool, optional): Whether or not to aggregate the coverage statistic in this class. Defaults to True.
            use_token_lengths (bool, optional): Whether or not to consider the token lengths when calculating
                coverage.

        Returns:
            float: Returns the coverage. If record is True, additionally stores token length statistics in this class.
        """
        # If there are no strings, we take the convention that all strings are covered.
        if not strs:
            return 1.0

        matches = [s for s in strs if self.covers(s, use_token_lengths=use_token_lengths)]
        cov_count = len(matches)

        if record:
            self.coverage_accumulator.accumulate(cov_count / len(strs))
            self._record_statistics(strs, matches)
            return self.coverage_accumulator.value()
        return float(cov_count / len(strs))

    def __str__(self) -> str:
        """String representation of this expression without length information."""
        return "".join([str(x) for x in self.token_list])

    def annotated_str(self) -> str:
        """String repesentation of this expression including length specification."""
        # Requries statistical information.
        return "".join([Expression._annotate_token(p, h) for p, h in zip(self.token_list, self.token_length_histogram)])

    @staticmethod
    def _annotate_token(t: TokenType, hist: Type[Histogram]) -> str:
        """Annotates a token with length specifiers.

        In more detail, A token, e.g. Token.LOWER = [a-z]+, will have a length
        specifier that accepts any valid length string that matches the pattern
        [a-z]. In this case "+" is used so any string of length >= 1 matching [a-z].
        This method will replace "+" by a specific length specifier, e.g. {2,3}
        that restricts the lengths of matching strings; in this case, to strings
        of length 2 or 3. So it will take Token.LOWER and return [a-z]{2,3}, for
        example.

        Args:
            t (TokenType): a token
            hist (Histogram): a histogram of observed token lengths.

        Returns:
            (str) a string regular expression with length specifiers
        """
        # No annotation for delimiters.
        if Tokens.is_delimiter(t.token):
            return t.token

        l, u = hist.range()
        if u is None:
            return t.token
        if u == l:
            length_range = str(u)
        else:
            length_range = "{}-{}".format(l, u)
        return str(t)[0:-1] + ":" + length_range + "}"

    @staticmethod
    def _length_range(hist: Type[Histogram]) -> str:
        """Takes a histogram of witnessed lengths and produces a length range,
        that is an ordered pair indicating the upper and lower lengths"""
        l, u = hist.range()

        if u is None:
            return None
        return l, u


ExpressionType = Type[Expression]


class ExpressionSet:
    """An expression set stores ranked expressions along with meta data for
    those expressions.

    Meta information that is stored includes witnessed token lengths. Ranking is
    determined using various metrics including coverage and token specificity.

    N.B. This class may be used in the future to implement a beam search,
    dropping lower ranking expressions. For now it stores every expression.
    """

    def __init__(self, min_coverage: float = 0.8):
        """Initializer for an expression set.

        Args:
            min_coverage (float, optional): An expresion set will omit any expression whose coverage falls below this
                number.
        """
        self.expressions = {}
        self.min_coverage = min_coverage
        self.num_experiments = 0
        self.sample_size = 0

    def ranked_expressions(self) -> Iterator[ExpressionType]:
        """Returns an iterator of ranked expressions from best to worst having a minimal coverage."""
        exprs = map(lambda x: x[1], sorted(self.expressions.items(), key=lambda item: item[1], reverse=True))
        return filter(lambda x: x.coverage_accumulator.value() >= self.min_coverage and str(x) != "{any}", exprs)

    def best_expression(self) -> ExpressionType:
        """Returns the top ranking expression in this class. A tie is broken deterministically arbitrarily."""
        expressions = list(self.ranked_expressions())
        if expressions and expressions[0].coverage_accumulator.value() >= self.min_coverage:
            return expressions[0]
        return None

    def combine(self, exprs: Union[List[str], Set[str]]) -> None:
        """This method takes a new set of expressions and merges those
        expressions into this data set.

        Any statistics (witnessed token lengths, coverages) will be aggregated
        into the expression set.  N.B. This class will take ownership of the
        expressions. In other words it will not copy expressions, it will point
        to expressions to reduce memory churn.

        Args:
            exprs ((List/Set) of Expression): A list of expressions to merge
            into this data structure.
        """
        for expr in exprs:
            expr_str = str(expr)

            # If the expression is not currently in the expression set, simply add it.
            if expr_str not in self.expressions:
                self.expressions[expr_str] = expr

            # If the expression is in the expression set, merge any statistics.
            elif expr_str in self.expressions:
                # Specificity will be equal. Coverage should be merged, and token histogram should be merged.
                # This code should go elsewhere for separation of concerns.

                # Combine the statistics for witnessed token lengths, matches
                # and outliers.
                curr_expr = self.expressions[expr_str]
                # 1) Witnessed token lengths
                for h, j in zip(expr.token_length_histogram, curr_expr.token_length_histogram):
                    h.merge(j)

                # 2) Matches and outliers
                expr.matches_histogram.merge(curr_expr.matches_histogram)
                expr.outliers_histogram.merge(curr_expr.outliers_histogram)

                # Merge the coverage statistics.
                expr.coverage_accumulator.accumulate(curr_expr.coverage_accumulator)

                # Overwrite the expression with the new one.
                self.expressions[expr_str] = expr

                # We can delete the old expression now.
                del curr_expr

    def record_experiment(self, num_strs):
        """Records how many experiments were run and on how many strings."""
        self.sample_size += num_strs
        self.num_experiments += 1

    def experiment_statistics(self):
        """Returns statistics on the number of experiments and number of strings inspected."""
        return self.num_experiments, self.sample_size

    def print_summary(self, min_coverage: float = 0.20, display_histogram: bool = False):
        """A debugging method to print summary informatio about this expression set."""

        if display_histogram:
            print("Pattern\t\t\t\tCoverage (>= {}) \tSpecificity\tHistogram of Token Lengths".format(min_coverage))
        else:
            print("Pattern\t\t\t\tCoverage (>= {}) \tSpecificity".format(min_coverage))

        for v in self.ranked_expressions():
            if v.coverage_accumulator.value() < min_coverage:
                continue
            if display_histogram:
                print(
                    "{} {:.3f}\t\t{:.2f}\t\t{}".format(
                        "{0:<35}".format(v.annotated_str()),
                        v.coverage_accumulator.value(),
                        v.specificity,
                        ", ".join([str(h) for h in v.token_length_histogram]),
                    )
                )
            else:
                print(
                    "{} {:.3f}\t\t{:.2f}".format(
                        "{0:<35}".format(v.annotated_str()), v.coverage_accumulator.value(), v.specificity
                    )
                )


ExpressionSetType = Type[ExpressionSet]
