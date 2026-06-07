from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.core_model import Model, ModelInputData


@dataclass
class PlayerRegistrationInputData(ModelInputData):
    chess_id: str
    tournament_pk: str


@dataclass
class PlayerRegistration(Model[PlayerRegistrationInputData]):
    pk: str
    chess_id: str
    tournament_pk: str

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> PlayerRegistration:
        player_registration = cls(
            pk=json_data["pk"],
            chess_id=json_data["chess_id"],
            tournament_pk=json_data["tournament_pk"],
        )
        return player_registration

    def to_json(self) -> dict[str, Any]:
        json: dict[str, Any] = {
            "pk": self.pk,
            "chess_id": self.chess_id,
            "tournament_pk": self.tournament_pk,
        }
        return json

    @classmethod
    def from_user_input(
        cls, new_pk: str, user_input: PlayerRegistrationInputData
    ) -> PlayerRegistration:
        player_registration = cls(
            pk=new_pk,
            chess_id=user_input.chess_id,
            tournament_pk=user_input.tournament_pk,
        )
        return player_registration
