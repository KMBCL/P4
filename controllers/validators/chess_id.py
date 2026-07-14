"""Validates the national chess identifier of a player."""

import re


from core.result import Result
from core.core_formats import CHESS_ID, CHESS_ID_HINT


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
                - An invalid one whose reason states the expected format.
        """
        chess_id = re.fullmatch(CHESS_ID, user_input)
        if chess_id is None:
            return Result.invalid(f"Invalid format - Expected '{CHESS_ID_HINT}'")

        return Result.valid(value=chess_id)
