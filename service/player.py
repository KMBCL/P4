from typing import Any, TypeAlias
from pathlib import Path
from core.result import Result

from core.core_data_repository import (
    PLAYER_DIR,
    CoreDataRepository,
)
from models.player import Player

Players: TypeAlias = list[Player]


class PlayerService:

    def __init__(self) -> None:
        self.repository = CoreDataRepository[Player](Player)
        self.repository.data_path = PLAYER_DIR

    def make_key(self, player: Player) -> str:
        return f"{player.last_name}-{player.first_name}-{player.chess_id}".lower()

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
