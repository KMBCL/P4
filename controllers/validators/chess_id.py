from typing import Any
import re


from controllers.result import Result


class ChessIDValidator:
    CHESS_ID_MAX_CHARACTERS = 7
    CHESS_ID_MAX_LETTERS_GROUP = 2
    CHESS_ID_MAX_NUMBERS_GROUP = 5

    def validate_chess_id(self, user_input: str) -> Result:
        chess_id = re.fullmatch(r"([A-Za-z]{2})(\d{5})", user_input)
        if chess_id is None:
            return Result.invalid("Invalid format - Expected 'AA00000'")

        return Result.valid()
