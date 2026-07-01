from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from core.core_model import Model
from core.constants import WinningCondition
from models.score import PlayerScore
from models.player import Player

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
class RoundMatch(Model[Any]):
    player_score_a: PlayerScore
    player_score_b: PlayerScore

    def calculate_match_score(self) -> float:
        # return self.score_a.score_value + self.score_b.score_value
        pass

    def is_score_complete(self):
        return self.calculate_match_score() == SCORE

    def give_score_b_value(self, winning_condition: WinningCondition) -> float:
        if winning_condition == WinningCondition.VICTORY:
            return DEFEAT_SCORE

        if winning_condition == WinningCondition.DEFEAT:
            return VICTORY_SCORE

        return DRAW_SCORE

    def set_score(self, winning_condition: WinningCondition):
        # self.score_a.score_value = SCORE_DEFINITION.get(winning_condition, DEFEAT_SCORE)
        # self.score_b.score_value = self.give_score_b_value(winning_condition)
        pass

    def to_list(self) -> list[PlayerScore]:
        return [self.player_score_a, self.player_score_b]


def default_matches() -> list[RoundMatch]:
    return []


def default_raw_matches() -> list[list[str]]:
    return []


@dataclass
class Round(Model[Any]):
    name: str
    start_timestamp: str
    end_timestamp: str
    round_matches_payload: list[list[str]] = field(default_factory=default_raw_matches)
    round_matches: list[RoundMatch] = field(default_factory=default_matches)

    def set_round_players(self, player_pairs: list[tuple[Player, Player]]) -> None:
        round_matches: list[RoundMatch] = [
            RoundMatch(
                player_score_a=PlayerScore(player=player_a),
                player_score_b=PlayerScore(player=player_b),
            )
            for player_a, player_b in player_pairs
        ]
        self.round_matches = round_matches

    def set_round_matches_from_payload(self, round_matches: list[RoundMatch]) -> None:
        self.round_matches = round_matches

    def are_round_matches_defined(self) -> bool:
        return bool(self.round_matches)

    def is_round_score_complete(self) -> bool:
        total_score = 0
        for round_match in self.round_matches:
            match_score = round_match.calculate_match_score()
            total_score = total_score + match_score

        return total_score == len(self.round_matches) * SCORE
