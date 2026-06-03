from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.core_model import Model


@dataclass
class PlayerInputData:
    chess_id: str
    last_name: str
    first_name: str
    birthdate: str


@dataclass
class Player(Model):
    pk: int
    chess_id: str
    last_name: str
    first_name: str
    birthdate: str

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Player:
        player = cls(
            pk=json_data["pk"],
            chess_id=json_data["chess_id"],
            last_name=json_data["last_name"],
            first_name=json_data["first_name"],
            birthdate=json_data["birthdate"],
        )
        return player

    def to_json(self) -> dict[str, Any]:
        json: dict[str, Any] = {
            "pk": self.pk,
            "chess_id": self.chess_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birthdate": self.birthdate,
        }
        return json

    @classmethod
    def from_player_input(cls, new_pk: int, player_input: PlayerInputData) -> Player:
        player = cls(
            pk=new_pk,
            chess_id=player_input.chess_id,
            last_name=player_input.last_name,
            first_name=player_input.first_name,
            birthdate=player_input.birthdate,
        )
        return player
