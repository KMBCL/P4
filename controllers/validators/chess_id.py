import re


from core.result import Result


class ChessIDValidator:

    @staticmethod
    def validate_chess_id(user_input: str) -> Result:
        chess_id = re.fullmatch(r"([A-Za-z]{2})(\d{5})", user_input)
        if chess_id is None:
            return Result.invalid("Invalid format - Expected 'AA00000'")

        return Result.valid(value=chess_id)
