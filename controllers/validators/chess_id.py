from dataclasses import dataclass
import re

from controllers.result import Result


@dataclass
class ChessID:
    letters_group: str
    numbers_group: str


class ChessIDValidator:
    CHESS_ID_MAX_CHARACTERS = 7
    CHESS_ID_MAX_LETTERS_GROUP = 2
    CHESS_ID_MAX_NUMBERS_GROUP = 5

    def validate_chess_id_max_characters(self, chess_id: str) -> Result:
        if len(chess_id) != self.CHESS_ID_MAX_CHARACTERS:
            return Result.invalid(
                f"Incorrect chess id : {chess_id} - Expected 'AA00000'"
            )
        return Result.valid()

    def validate_chess_id_max_letter(self, letters_group: str) -> Result:
        if len(letters_group) != self.CHESS_ID_MAX_LETTERS_GROUP:
            return Result.invalid(
                f"Incorrect chess id letters group : {letters_group} - Expected 'AA'"
            )
        return Result.valid()

    def split_chess_id(self, user_input: str) -> ChessID | None:
        match = re.fullmatch(r"([A-Za-z]+)(\d+)", user_input)

        if not match:
            return None

        chess_id = ChessID(
            letters_group=match.group(1),
            numbers_group=match.group(2),
        )
        return chess_id

    def validate_chess_id(self, user_input: str) -> Result:
        max_characters_result = self.validate_chess_id_max_characters(user_input)
        if not max_characters_result:
            return max_characters_result

        chess_id = self.split_chess_id(user_input)
        if chess_id is None:
            return Result.invalid("Invalid format - Expected 'AA00000'")

        max_letters_group_result = self.validate_chess_id_max_letter(
            chess_id.letters_group
        )
        if not max_letters_group_result:
            return max_letters_group_result

        return Result.valid()
