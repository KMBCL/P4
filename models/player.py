from __future__ import annotations

from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, Any

from datetime import date

from repository.data import DataItem


@dataclass
class PlayerInputData:
    chess_id: str
    last_name: str
    first_name: str

    def serialize_data(self) -> str:
        serialized_data = f"chess_id={self.chess_id}, last_name={self.last_name}, first_name={self.first_name}"
        return serialized_data


@dataclass
class Player:
    pk: int
    chess_id: str
    last_name: str
    first_name: str
    birthdate: date | None = None

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Player:
        player = cls(
            pk=json_data["pk"],
            chess_id=json_data["chess_id"],
            last_name=json_data["last_name"],
            first_name=json_data["first_name"],
        )
        return player

    def _to_content(self) -> str:
        EXCEPT = ["pk", "birthdate"]
        content: str = ""
        for field in fields(self):
            if field.name in EXCEPT:
                continue

            content = content + " - " if content else content
            content = content + f"{field.name}={getattr(self,field.name)}"
        return content

    def to_data_item(self) -> DataItem:
        return DataItem(shortcut=str(self.pk), content=self._to_content())

    @classmethod
    def from_player_input(cls, new_pk: int, player_input: PlayerInputData) -> Player:
        player = cls(
            pk=new_pk,
            chess_id=player_input.chess_id,
            last_name=player_input.last_name,
            first_name=player_input.first_name,
        )
        return player

    def to_json(self) -> dict[str, Any]:
        json: dict[str, Any] = {
            "pk": self.pk,
            "chess_id": self.chess_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
        }
        return json
