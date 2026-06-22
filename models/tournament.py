from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.core_model import Model, ModelInputData

from models.helpers.flat import flat_rounds, flat_scores

from models.round import Round, RoundMatch


@dataclass
class TournamentInputData(ModelInputData):
    name: str
    place: str
    start_date: str
    end_date: str
    description: str
    round_count: str


def default_registered_players_chess_id() -> list[str]:
    registered_player_chess_ids: list[str] = []
    return registered_player_chess_ids


def default_rounds() -> list[Round]:
    rounds: list[Round] = []
    return rounds


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
    registered_player_chess_ids: list[str] = field(
        default_factory=default_registered_players_chess_id
    )
    rounds: list[Round] = field(default_factory=default_rounds)

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Tournament:
        tournament = cls(
            pk=json_data["pk"],
            name=json_data["name"],
            place=json_data["place"],
            start_date=json_data["start_date"],
            end_date=json_data["end_date"],
            description=json_data["description"],
            player_count=len(json_data["registered_player_chess_ids"]),
            round_count=json_data["round_count"],
            registered_player_chess_ids=json_data["registered_player_chess_ids"],
            rounds=[Round.from_json(data) for data in json_data["rounds"]],
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
            "registered_player_chess_ids": self.registered_player_chess_ids,
            "rounds": [round.to_json() for round in self.rounds],
        }
        return json

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
            registered_player_chess_ids=[],
            rounds=cls.add_rounds(int(user_input.round_count)),
        )
        return tournament

    def get_round(self, round_name: str) -> Round | None:
        for round in self.rounds:
            if round.name == round_name:
                return round

        return None

    def update_round_matches(self, round_matches: list[RoundMatch], round_name: str):
        self.rounds = [
            (
                round.set_round_matches(round_matches)
                if round.name == round_name
                else round
            )
            for round in self.rounds
        ]

    def sort_player_scores(self, player_scores: dict[str, float]) -> dict[str, float]:
        return dict(
            sorted(
                player_scores.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

    def get_player_scores(self) -> dict[str, float]:
        player_scores: dict[str, float] = {}
        round_matches = flat_rounds(self.rounds)
        scores = flat_scores(round_matches)
        for score in scores:
            if player_scores.get(score.chess_id, None) is None:
                player_scores[score.chess_id] = score.score_value
                continue

            player_scores[score.chess_id] += score.score_value

        sorted_players = self.sort_player_scores(player_scores)
        return sorted_players

    @property
    def has_begun(self) -> bool:
        round_matches = [round.round_matches for round in self.rounds]
        return bool(round_matches)
