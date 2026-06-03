from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.core_model import Model


@dataclass
class TournamentInputData:
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    round_count: str


@dataclass
class Tournament(Model):
    pk: int
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    round_count: int = 4

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Tournament:
        tournament = cls(
            pk=json_data["pk"],
            name=json_data["name"],
            place=json_data["place"],
            start_date=json_data["start_date"],
            end_date=json_data["end_date"],
            description=json_data["description"],
            round_count=json_data["round_count"],
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
            "round_count": self.round_count,
        }
        return json

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
            round_count=int(user_input.round_count),
        )
        return tournament
