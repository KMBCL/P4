from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.core_model import Model

from models.score import PlayerScore
from models.player import Player

SCORE = 1
VICTORY_SCORE = 1.0
DEFEAT_SCORE = 0.0
DRAW_SCORE = 0.5


@dataclass
class RoundMatch(Model[Any]):
    player_score_a: PlayerScore
    player_score_b: PlayerScore

    def set_draw(self):
        self.player_score_a.score_value = DRAW_SCORE
        self.player_score_b.score_value = DRAW_SCORE

    def _set_score(self, player_score: PlayerScore, winner: Player) -> None:
        if player_score.player.chess_id == winner.chess_id:
            player_score.score_value = VICTORY_SCORE
        else:
            player_score.score_value = DEFEAT_SCORE

    def set_score(self, winner: Player | None) -> None:
        if winner is None:
            self.set_draw()
            return None

        self._set_score(self.player_score_a, winner)
        self._set_score(self.player_score_b, winner)

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
