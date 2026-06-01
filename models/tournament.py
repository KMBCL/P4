from __future__ import annotations

from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, Any

from datetime import date

from repository.data import DataItem


@dataclass
class TournamentInputData:
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    turn_count: str


@dataclass
class Tournament:
    pk: int
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    turn_count: int = 4

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Tournament:
        tournament = cls(
            pk=json_data["pk"],
            name=json_data["name"],
            place=json_data["place"],
            start_date=json_data["start_date"],
            end_date=json_data["end_date"],
            description=json_data["description"],
            turn_count=json_data["turn_count"],
        )
        return tournament

    def _to_content(self) -> str:
        EXCEPT = ["pk", "start_date", "end_date"]
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
    def from_user_input(
        cls, new_pk: int, user_input: TournamentInputData
    ) -> Tournament:
        tournament = cls(
            pk=new_pk,
            name=user_input.name,
            place=user_input.place,
            start_date=user_input.start_date,
            end_date=user_input.end_date,
            description=user_input.description,
            turn_count=int(user_input.turn_count),
        )
        return tournament

    def to_json(self) -> dict[str, Any]:
        json: dict[str, Any] = {
            "pk": self.pk,
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "turn_count": self.turn_count,
        }
        return json
