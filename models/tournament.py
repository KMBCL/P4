"""Provides the tournament domain model, the aggregate of the application."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from core.core_model import Model, ModelInputData

from models.round import Round

if TYPE_CHECKING:
    from models.player import Player


DEFAULT_ROUND_COUNT = 4


@dataclass
class TournamentInputData(ModelInputData):
    """Carries the raw tournament fields as they were typed by the user."""

    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    round_count: str


def default_registered_player_payload() -> list[str]:
    """Builds the default registered players of a tournament, as chess ids.

    Returns:
        list[str]: An empty list.
    """
    return []


def default_rounds() -> list[Round]:
    """Builds the default rounds of a tournament.

    Returns:
        list[Round]: An empty list.
    """
    return []


def default_players() -> list[Player]:
    """Builds the default players of a tournament.

    Returns:
        list[Player]: An empty list.
    """
    return []


@dataclass
class Tournament(Model[TournamentInputData]):
    """Runs a fixed number of rounds between the players registered to it."""

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
        """Builds one empty round, named after its position in the tournament.

        Args:
            index (int): The position of the round, counted from zero.

        Returns:
            Round: The new round, with no timestamp and no match.
        """
        round = Round(
            name="Round " + str(index),
            start_timestamp="",
            end_timestamp="",
            round_matches=[],
        )
        return round

    @classmethod
    def add_rounds(cls, round_count: int):
        """Builds every round of the tournament at once.

        Args:
            round_count (int): The number of rounds the tournament will run.

        Returns:
            list[Round]: The rounds, in the order they will be played.
        """
        rounds: list[Round] = [
            cls.new_round(index) for index in range(1, round_count + 1)
        ]
        return rounds

    @classmethod
    def from_user_input(
        cls, new_pk: str, user_input: TournamentInputData
    ) -> Tournament:
        """Builds a tournament from validated user input.

        Args:
            new_pk (str): The primary key assigned to the new tournament.
            user_input (TournamentInputData): The raw fields typed by the user.

        Returns:
            Tournament: The new tournament, with no player registered.
        """
        tournament = cls(
            pk=new_pk,
            name=user_input.name,
            place=user_input.place,
            start_date=user_input.start_date,
            end_date=user_input.end_date,
            description=user_input.description,
            round_count=user_input.round_count,
            registered_player_payload=[],
            rounds=cls.add_rounds(int(user_input.round_count or DEFAULT_ROUND_COUNT)),
        )
        return tournament
