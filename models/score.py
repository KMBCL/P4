from __future__ import annotations

from dataclasses import dataclass

from models.player import Player

INITIAL_SCORE: str = "0.0"
INITIAL_SCORE_VALUE: float = 0


@dataclass
class PlayerScore:
    player: Player
    score: str = INITIAL_SCORE

    @property
    def score_value(self) -> float:
        return float(self.score)

    @score_value.setter
    def score_value(self, value: float) -> None:
        self.score = str(value)

    @property
    def is_score_not_set(self) -> bool:
        return self.score == INITIAL_SCORE


@dataclass
class TournamentPlayerScore:
    player: Player
    _tournement_score_value: float = INITIAL_SCORE_VALUE

    def increment_score(self, score_value: float) -> None:
        self._tournement_score_value += score_value

    @property
    def tournement_score_value(self) -> float:
        return self._tournement_score_value
