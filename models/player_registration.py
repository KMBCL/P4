from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.core_model import Model


@dataclass
class PlayerRegistrationInputData:
    player_pk: str
    tournament_pk: str


@dataclass
class PlayerRegistration(Model):
    pk: int
    player_pk: str
    tournament_pk: str

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> PlayerRegistration:
        player_registration = cls(
            pk=json_data["pk"],
            player_pk=json_data["player_pk"],
            tournament_pk=json_data["tournament_pk"],
        )
        return player_registration

    def to_json(self) -> dict[str, Any]:
        json: dict[str, Any] = {
            "pk": self.pk,
            "player_pk": self.player_pk,
            "tournament_pk": self.tournament_pk,
        }
        return json

    @classmethod
    def from_user_input(
        cls, new_pk: int, user_input: PlayerRegistrationInputData
    ) -> PlayerRegistration:
        player_registration = cls(
            pk=new_pk,
            player_pk=user_input.player_pk,
            tournament_pk=user_input.tournament_pk,
        )
        return player_registration
