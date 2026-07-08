from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from core.core_model import Model, ModelInputData

from models.round import Round

if TYPE_CHECKING:
    from models.player import Player


@dataclass
class TournamentInputData(ModelInputData):
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    round_count: str


def default_registered_player_payload() -> list[str]:
    return []


def default_rounds() -> list[Round]:
    return []


def default_players() -> list[Player]:
    return []


@dataclass
class Tournament(Model[TournamentInputData]):
    pk: str
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    player_count: int = 0
    round_count: str = "4"
    registered_player_payload: list[str] = field(
        default_factory=default_registered_player_payload
    )
    registered_players: list[Player] = field(default_factory=default_players)
    rounds: list[Round] = field(default_factory=default_rounds)

    @classmethod
    def new_round(cls, index: int):
        round = Round(
            name="round_" + str(index),
            start_timestamp="",
            end_timestamp="",
            round_matches=[],
        )
        return round

    @classmethod
    def add_rounds(cls, round_count: int):
        rounds: list[Round] = [cls.new_round(index) for index in range(round_count)]
        return rounds

    @classmethod
    def from_user_input(
        cls, new_pk: str, user_input: TournamentInputData
    ) -> Tournament:
        tournament = cls(
            pk=new_pk,
            name=user_input.name,
            place=user_input.place,
            start_date=user_input.start_date,
            end_date=user_input.end_date,
            description=user_input.description,
            round_count=user_input.round_count,
            registered_player_payload=[],
            rounds=cls.add_rounds(int(user_input.round_count)),
        )
        return tournament
