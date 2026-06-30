from __future__ import annotations

from dataclasses import dataclass

from models.player import Player


@dataclass
class PlayerScore:
    player: Player
    score: str = "0.0"

    @property
    def score_value(self) -> float:
        return float(self.score)

    @score_value.setter
    def score_value(self, value: float) -> None:
        self.score = str(value)
