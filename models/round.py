from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self, TypeAlias

from core.core_model import Model, ModelInputData


@dataclass
class Score:
    chess_id: str
    score: float


@dataclass
class RoundMatch(Model[Any]):
    name: str
    score_a: Score
    score_b: Score

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Self:
        raw_scores = json_data["scores"]
        scores: list[Score] = [
            Score(chess_id=raw_score[0], score=raw_score[1]) for raw_score in raw_scores
        ]
        round_match = cls(
            name=json_data["name"],
            score_a=scores[0],
            score_b=scores[1],
        )
        return round_match


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
        raw_matches: list[dict[str, Any]] = json_data["round_matches"]
        round_matches: list[RoundMatch] = [
            RoundMatch.from_json(raw_match) for raw_match in raw_matches
        ]
        round = cls(
            name=json_data["name"],
            start_timestamp=json_data["start_timestamp"],
            end_timestamp=json_data["end_timestamp"],
            round_matches=round_matches,
        )
        return round
