"""Validates the national chess identifier of a player."""

import re


from core.result import Result


class ChessIDValidator:
    """Checks that a raw chess id has the expected shape."""

    @staticmethod
    def validate_chess_id(user_input: str) -> Result:
        """Validates a chess id against the 'AA00000' format.

        The expected format is two letters, upper or lower case, followed by
        exactly five digits.

        Args:
            user_input (str): The raw chess id typed by the user.

        Returns:
            Result:
                - A valid result carrying the ``re.Match``
                - A Invalid one whose reason states the expected format.
        """
        chess_id = re.fullmatch(r"([A-Za-z]{2})(\d{5})", user_input)
        if chess_id is None:
            return Result.invalid("Invalid format - Expected 'AA00000'")

        return Result.valid(value=chess_id)
