from dataclasses import dataclass
from typing import Any, TypeAlias
from pathlib import Path
import json

from repository.data import DATA_BASE_ROOT, DataSet, DataItem, DataRepository
from models.player import Player

Players: TypeAlias = list[Player]


class PlayerRepository(DataRepository):
    data_path: Path

    def __init__(self) -> None:
        self.data_path = Path(f"{DATA_BASE_ROOT}/players.json")

    def read_json_file(self) -> list[dict[str, Any]]:
        with self.data_path.open("r", encoding="utf-8") as file:
            return json.load(file)

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

    def get_data(self) -> DataSet:
        data_set: list[DataItem] = []

        players = self.get_players()

        for player in players:
            data_set.append(player.to_data_item())

        return DataSet(data_set)

    def write_data(self, json_data: dict[str, Any]):
        players = self.read_json_file()
        players.append(json_data)

        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(players, file, indent=4, ensure_ascii=False)
