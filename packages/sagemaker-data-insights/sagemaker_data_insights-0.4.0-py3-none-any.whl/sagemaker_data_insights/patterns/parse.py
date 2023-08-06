from typing import List

from .tokens import TokenType, Tokens


class Parse:
    """
    Methods to parse tokens from strings.
    """

    @staticmethod
    def parse_token(s: str) -> TokenType:
        """Return the most appropriate token for a string.
        Args:
            s (str): A string (can be anything).

        Returns:
            Token: The best match token for the string (delimiters/semantic type). See Tokens class.
        """
        for t in Tokens.SEPARATOR_TYPES:
            if t.match(s):
                return t
        for t in Tokens.SEMANTIC_TYPES:
            if t.match(s):
                return t
        return Tokens.ANY

    @staticmethod
    def parse(s: str) -> List[TokenType]:
        """Parse a string into a list of tokens (including delimiters).

        Args:
            s (str): A string.

        Returns:
            List[Tokens]: The list of tokens that compose the string.
        """
        ts = Tokens.split_by_delimiters(s)
        return [Parse.parse_token(t) for t in ts]
