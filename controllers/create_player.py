from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
from enum import StrEnum
import re

from controllers.result import Result
from models.player import Player, PlayerInputData
from repository.player import PlayerRepository


class PlayerShortcuts(StrEnum):
    CREATE_PLAYER = "CP"
    PLAYERS = "PS"


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
                f"Incorrect chess id : {chess_id} - Expected 'AA00000"
            )
        return Result.valid()

    def validate_chess_id_max_letter(self, letters_group: str) -> Result:
        if len(letters_group) != self.CHESS_ID_MAX_LETTERS_GROUP:
            return Result.invalid(
                f"Incorrect chess id letters group : {letters_group} - Expected 'AA'"
            )
        return Result.valid()

    def validate_chess_id_max_numbers_group(self, numbers_group: str) -> Result:
        if len(numbers_group) != self.CHESS_ID_MAX_NUMBERS_GROUP:
            return Result.invalid(
                f"Incorrect chess id numbers group : {numbers_group} - Expected '00000'"
            )
        return Result.valid()

    def split_chess_id(self, user_input: str) -> ChessID:
        match = re.fullmatch(r"([A-Za-z]+)(\d+)", user_input)

        if not match:
            raise ValueError("Format invalide")

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

        max_letters_group_result = self.validate_chess_id_max_letter(
            chess_id.letters_group
        )
        if not max_letters_group_result:
            return max_letters_group_result

        max_numbers_group_result = self.validate_chess_id_max_numbers_group(
            chess_id.numbers_group
        )
        if not max_numbers_group_result:
            return max_numbers_group_result

        return Result.valid()


class PlayerController(ChessIDValidator):

    def __init__(self) -> None:
        self.view = None
        self.repository = PlayerRepository()

    def validate_input_action(self, user_input: str) -> bool:
        return user_input in PlayerShortcuts

    def build_new_player(self, player_input: PlayerInputData, new_pk: int):
        new_player = Player.from_player_input(new_pk=new_pk, player_input=player_input)
        return new_player

    def make_new_pk(self, repository: PlayerRepository):
        new_pk = repository.get_data().new_pk()
        return new_pk

    def create_new_player(self, player_input: PlayerInputData) -> str:
        new_pk = self.make_new_pk(repository=self.repository)
        player = self.build_new_player(
            player_input=player_input,
            new_pk=new_pk,
        )
        self.repository.write_data(json_data=player.to_json())
        return "success!"

    def get_players(self):
        return self.repository.get_players()
