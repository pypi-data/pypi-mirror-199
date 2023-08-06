import re
from typing import List, Type, Tuple, Optional


LengthSpecifier = Tuple[int, int]


class Token:
    """A class to store tokens for pattern recognition..

    This class represents a single token and contains information to generate
    the equivalent regular expression for this token. The reason we have this
    class is to natively express the simplified context-free grammar for Pattern
    learning. This CFG is contained within the language of all regular
    expressions. Thus each token has a regular expression.

    N.B. Each instantiation of this class is meant to be a singleton class, and
    there is exactly one instantiation for each Token. This is by design to
    reduce memory churn. You should not be instantiating this class outside of
    the Tokens class.
    """

    def __init__(
        self,
        token: str,
        token_regex: str = "",
        head_length: int = 0,
        length_specifier: Optional[LengthSpecifier] = None,
        specificity: int = None,
    ):
        """Initializer for Token.

        Tokens consist of an optional head regular expression that is matched
        exactly once followed by a base regular expression that is repeated a
        specified number of times. The token regex is the head, concatenated by
        the base, followed by the length specifier.

        Example 1. To match one or more digits,
            Token = {digits}
            Token Regex: [0-9]
            Head Length: 0
            Length Specifier = +
        Giving the call: Token('{digits}', base_regex='[0-9]', base_length_specifier='+')


        Example 2. To match a capitalized word,
            Token = {name}
            Token regex: [A-Z][a-z]
            Head length: 1
            Length Specifier = +
        Giving the call: Token('{name}', head_regex='[A-Z]', base_regex='[a-z]', base_length_specifier='+')


        Example 3. To match a delimiter character
            Token = ',' (the literal)
            Token regex = ',' (the literal)
            Head length: 0
            Length Specifier = None
        Giving the call Token(',', base_regex=',')

        Args:
            token (str): The string representation of this token. Conventially we surrounded by braces for semantic
                types.
            token_regex (str): The main regular expression that may be repeated a number of times.
            head_length (int, optional): The number of characters of the head of the regex.
            base_length_specifier (int, optional): A specifier (e.g. '+', '*', {2,3}) for the number of times the
                base_regex can be repeated.
            specificity (int): A ranked measure of how specific the token is.
            base_length_specifier (str, optional): A specifier, either '+' or '*' that is appended to the regular
                expression specify the length of a match.
        """
        self.token = token
        self.token_regex = token_regex
        self.head_length = head_length
        self.length_specifier = length_specifier
        self.specificity = specificity

    def regex(self, length_specifier: Optional[LengthSpecifier] = None) -> str:
        """Returns the regular expression for this token with the ability to override the default length specifier.

        Args:
            range (pair of int, optional): A pair of lower and upper token lengths. Defaults to None.

        Returns:
            str: A string representation of the regular expression for this token.
        """
        if self.length_specifier is None:
            # Length specification for delimiters is ignored.
            return self.token_regex
        if length_specifier is None:
            # No range specified, so use the default length specifier.
            return f"{self.token_regex}{self.length_specifier}"

        # A length specifier is given. Update it to account for the (required) head length.
        lower = length_specifier[0] - self.head_length
        upper = length_specifier[1] - self.head_length

        if upper <= 1:
            return f"{self.token_regex}"
        if lower == upper:
            return f"{self.token_regex}{{{lower}}}"
        return f"{self.token_regex}{{{lower},{upper}}}"

    def match(self, target, length_range=None):
        """Indicates whether or not the token matches the target, using the specified range"""
        # TODO: We can optimize this by memoization.
        return re.fullmatch(self.regex(length_specifier=length_range), target)

    def __str__(self):
        """Returns the token string representation."""
        return self.token


TokenType = Type[Token]


class Tokens:
    """A class containing all the Token category types for semantic types and delimiters and some related methods."""

    # Definitions of semantic types.
    # N.B. In future versions we will add additional simple types such as
    # {TitleCase} | {camelCase} | {snake-case}
    # as well as more complex types such as e-mail address, IP Address, etc.
    ANY = Token("{any}", token_regex="\\w", specificity=0, length_specifier="*")
    ALPHANUM = Token("{alnum}", token_regex="[A-Za-z0-9]", specificity=1, length_specifier="*")
    MIXED = Token("{mixed}", token_regex="[A-Za-z]", specificity=2, length_specifier="*")
    LOWER = Token("{lower}", token_regex="[a-z]", specificity=3, length_specifier="*")
    UPPER = Token("{upper}", token_regex="[A-Z]", specificity=3, length_specifier="*")
    NAME = Token("{name}", token_regex="[A-Z][a-z]", head_length=1, specificity=4, length_specifier="*",)
    DIGITS = Token("{digits}", token_regex="[0-9]", specificity=5, length_specifier="*")

    # Semantic types from highest to lowest specificity.
    SEMANTIC_TYPES = [DIGITS, NAME, UPPER, LOWER, MIXED, ALPHANUM, ANY]

    # Definitions of delimiter types.
    DELIM_COMMA = Token(",", token_regex=",", specificity=10)
    DELIM_HYPHEN = Token("-", token_regex="\\-", specificity=10)
    DELIM_DOUBLE_QUOTE = Token('"', token_regex='"', specificity=10)
    DELIM_NEWLINE = Token("{newline}", token_regex="\\n", specificity=10)
    DELIM_LEFT_BRACE = Token("[", token_regex="\\[", specificity=10)
    DELIM_LEFT_PAREN = Token("(", token_regex="\\(", specificity=10)
    DELIM_BACKWARD_SLASH = Token("\\", token_regex="\\\\", specificity=10)
    DELIM_PERIOD = Token(".", token_regex="\\.", specificity=10)
    DELIM_RIGHT_BRACE = Token("]", token_regex="\\]", specificity=10)
    DELIM_RIGHT_PAREN = Token(")", token_regex="\\)", specificity=10)
    DELIM_RIGHT_HYPHEN = Token("-", token_regex="\\-", specificity=10)
    DELIM_COLON = Token(":", token_regex=":", specificity=10)
    DELIM_SEMIC = Token(";", token_regex=";", specificity=10)
    DELIM_SINGLE_QUOTE = Token("'", token_regex="'", specificity=10)
    DELIM_SPACE = Token(" ", token_regex=" ", specificity=10)
    DELIM_TAB = Token("{tab}", token_regex="\t", specificity=10)
    DELIM_FORWARD_SLASH = Token("/", token_regex="/", specificity=10)

    # Separator types from highest to lowest specificity.
    SEPARATOR_TYPES = [
        DELIM_COMMA,
        DELIM_HYPHEN,
        DELIM_DOUBLE_QUOTE,
        DELIM_NEWLINE,
        DELIM_LEFT_BRACE,
        DELIM_LEFT_PAREN,
        DELIM_BACKWARD_SLASH,
        DELIM_PERIOD,
        DELIM_RIGHT_BRACE,
        DELIM_RIGHT_PAREN,
        DELIM_RIGHT_HYPHEN,
        DELIM_COLON,
        DELIM_SEMIC,
        DELIM_SINGLE_QUOTE,
        DELIM_SPACE,
        DELIM_TAB,
        DELIM_FORWARD_SLASH,
    ]
    DELIMITER_LIST = [str(d) for d in SEPARATOR_TYPES]
    DELIMITER_REGEX = f"[{''.join([x.regex() for x in SEPARATOR_TYPES])}]"
    SPLIT_BY_DELIMS_REGEX = re.compile(DELIMITER_REGEX)
    SPLIT_WITH_DELIMS_REGEX = re.compile(f"({DELIMITER_REGEX})")

    @staticmethod
    def is_delimiter(token: str) -> bool:
        """Is the token a delimiter"""
        return token in Tokens.DELIMITER_LIST

    @staticmethod
    def split_by_delimiters(s, keep_delimiters: bool = True) -> List[str]:
        """Splits based on a list of delimiters.

        Args:
            keep_delimiters: Whether or not to keep the delimiters in the split.
            delimiters: the list of delimiters (by default all delimiters in the class)

        Returns:
            A list of substrings split by the delimiters.
        """
        if keep_delimiters:
            splits = Tokens.SPLIT_WITH_DELIMS_REGEX.split(s)
        else:
            splits = Tokens.SPLIT_BY_DELIMS_REGEX.split(s)

        # re.split returns empty strings in the split so that it is the inverse function
        # of re.join. We remove those empty strings for the intended split behavior.
        return list(filter(lambda x: len(x) > 0, splits))
