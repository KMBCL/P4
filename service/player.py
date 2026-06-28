from typing import Any, TypeAlias
from pathlib import Path
from core.result import Result

from core.core_data_repository import (
    PLAYER_DIR,
    CoreDataRepository,
)
from models.player import Player, PlayerInputData

Players: TypeAlias = list[Player]


class PlayerService:

    def __init__(self) -> None:
        self.repository = CoreDataRepository[Player](Player)
        self.repository.data_path = PLAYER_DIR

    def get_player_by_name(self, player_name: str) -> Result:
        players = self.repository.get_models()
        similar_players = [
            player
            for player in players
            if player_name.lower() in player.last_name.lower()
        ]
        if not similar_players:
            return Result.invalid(
                reason=f"No players found with {player_name} last_name"
            )

        return Result.valid(value=similar_players)

    def can_save(self, chess_id: str) -> Result:
        filter: dict[str, str] = {"chess_id": chess_id}
        players = self.repository.get_filtered_models(filter)
        if players:
            return Result.invalid(
                reason=f"Found existing players {players} with same chess_id {chess_id}"
            )

        return Result.valid()

    def create_new_player(self, player_input: PlayerInputData) -> Result:
        can_save_resut = self.can_save(player_input.chess_id)
        if not can_save_resut:
            return can_save_resut

        self.repository.save_new_model(player_input)
        return Result.valid(success_message="Successfully saved new player!")

    def get_players(self) -> Result:
        players = self.repository.get_models()
        if not players:
            return Result.invalid("No players found")

        return Result.valid(players)
