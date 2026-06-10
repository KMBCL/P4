from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self, TypeAlias

from core.core_model import Model, ModelInputData
from core.constants import WinningCondition

SCORE = 1
VICTORY_SCORE = 1.0
DEFEAT_SCORE = 0.0
DRAW_SCORE = 0.5

SCORE_DEFINITION = {
    WinningCondition.VICTORY: VICTORY_SCORE,
    WinningCondition.DEFEAT: DEFEAT_SCORE,
    WinningCondition.DRAW: DRAW_SCORE,
}


@dataclass
class Score:
    chess_id: str
    score: str = "0.0"

    @property
    def score_value(self) -> float:
        return float(self.score)

    @score_value.setter
    def score_value(self, value: float) -> None:
        self.score = str(value)


@dataclass
class RoundMatch(Model[Any]):
    score_a: Score
    score_b: Score

    @classmethod
    def from_json_list(cls, json_data: list[str]) -> Self:
        scores: list[Score] = [
            Score(chess_id=raw_score[0], score=raw_score[1]) for raw_score in json_data
        ]
        round_match = cls(
            score_a=scores[0],
            score_b=scores[1],
        )
        return round_match

    def round_match_to_json(self) -> list[list[str]]:
        json: list[list[str]] = [
            [
                self.score_a.chess_id,
                self.score_a.score,
            ],
            [
                self.score_b.chess_id,
                self.score_b.score,
            ],
        ]
        return json

    def calculate_match_score(self) -> float:
        return self.score_a.score_value + self.score_b.score_value

    def is_score_complete(self):
        return self.calculate_match_score() == SCORE

    def give_score_b_value(self, winning_condition: WinningCondition) -> float:
        if winning_condition == WinningCondition.VICTORY:
            return DEFEAT_SCORE

        if winning_condition == WinningCondition.DEFEAT:
            return VICTORY_SCORE

        return DRAW_SCORE

    def set_score(self, winning_condition: WinningCondition):
        self.score_a.score_value = SCORE_DEFINITION.get(winning_condition, DEFEAT_SCORE)
        self.score_b.score_value = self.give_score_b_value(winning_condition)


def default_matches():
    default_matches: list[RoundMatch] = []
    return default_matches


@dataclass
class Round(Model[Any]):
    name: str
    start_timestamp: str
    end_timestamp: str
    round_matches: list[RoundMatch] = field(default_factory=default_matches)

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Self:
        raw_matches: list[list[str]] = json_data["round_matches"]
        round_matches: list[RoundMatch] = [
            RoundMatch.from_json_list(raw_match) for raw_match in raw_matches
        ]
        round = cls(
            name=json_data["name"],
            start_timestamp=json_data["start_timestamp"],
            end_timestamp=json_data["end_timestamp"],
            round_matches=round_matches,
        )
        return round

    def to_json(self) -> dict[str, Any]:
        json: dict[str, Any] = {
            "name": self.name,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "round_matches": [
                round_match.round_match_to_json() for round_match in self.round_matches
            ],
        }
        return json

    def set_round_players(self, player_pairs: list[tuple[str, str]]) -> None:
        round_matches: list[RoundMatch] = [
            RoundMatch(
                score_a=Score(chess_id=player_a), score_b=Score(chess_id=player_b)
            )
            for player_a, player_b in player_pairs
        ]
        self.round_matches = round_matches

    def set_round_matches(self, round_matches: list[RoundMatch]) -> Self:
        self.round_matches = round_matches
        return self

    def are_round_matches_defined(self) -> bool:
        return bool(self.round_matches)

    def is_round_score_complete(self) -> bool:
        total_score = 0
        for round_match in self.round_matches:
            match_score = round_match.calculate_match_score()
            total_score = total_score + match_score

        return total_score == len(self.round_matches) * SCORE
