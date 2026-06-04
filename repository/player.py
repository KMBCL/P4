from typing import Any, TypeAlias
from pathlib import Path


from core.core_data_repository import (
    DATA_BASE_ROOT,
    CoreDataRepository,
)
from models.player import Player, PlayerInputData

Players: TypeAlias = list[Player]


class PlayerRepository(CoreDataRepository):

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

    def get_player_by_pk(self, pk: str) -> Player | None:
        players = self.get_players()
        for player in players:
            if player.pk == int(pk):
                return player
        return None

    def get_filtered_players(self, filters: dict[str, Any]) -> Players:
        players = self.get_players()
        filtered_players: list[Player] = []
        field_name, field_value = next(iter(filters.items()))

        for player in players:
            try:
                player_attr: str = str(getattr(player, field_name)).lower()
            except AttributeError:
                continue

            if player_attr == field_value.lower():
                filtered_players.append(player)

        return filtered_players

    def save_new_player(self, player_input: PlayerInputData) -> None:
        player = Player.from_player_input(
            new_pk=self.make_new_pk(),
            player_input=player_input,
        )
        self.write_data(json_data=player.to_json())
