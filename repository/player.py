from dataclasses import dataclass
from typing import Any, TypeAlias
from pathlib import Path
import json

from repository.data import DATA_BASE_ROOT, DataSet, DataItem, DataRepository
from models.player import Player

Players: TypeAlias = list[Player]


class PlayerRepository(DataRepository):

    def __init__(self) -> None:
        self.data_path = Path(f"{DATA_BASE_ROOT}/players.json")

    def convert_to_player(self, raw_data: list[dict[str, Any]]) -> Players:
        players: Players = []

        for player_data in raw_data:
            player = Player.from_json(player_data)
            players.append(player)

        return players

    def get_players(self) -> Players:
        raw_data = self.read_json_file()
        players = self.convert_to_player(raw_data)
        return players
