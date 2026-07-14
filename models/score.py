"""Provides the scores of a player, within a match and across a tournament."""

from __future__ import annotations

from dataclasses import dataclass

from models.player import Player

INITIAL_SCORE: str = "0.0"
INITIAL_SCORE_VALUE: float = 0


@dataclass
class PlayerScore:
    """Holds the score of one player in one match, stored as a string."""

    player: Player
    score: str = INITIAL_SCORE

    @property
    def score_value(self) -> float:
        """Reads the score as a number.

        Returns:
            float: score converted from string.
        """
        return float(self.score)

    @score_value.setter
    def score_value(self, value: float) -> None:
        """Writes the score from a number.

        Args:
            value (float): score to store.
        """
        self.score = str(value)

    @property
    def is_score_not_set(self) -> bool:
        """Tells whether the match has been played. An unplayed match holds the initial score constant.

        Returns:
            bool: True when the score is still the initial score.
        """
        return self.score == INITIAL_SCORE


@dataclass
class TournamentPlayerScore:
    """Accumulates the scores won by one player over a whole tournament."""

    player: Player
    _tournament_score_value: float = INITIAL_SCORE_VALUE

    def increment_score(self, score_value: float) -> None:
        """Adds the score of one match to the running total.

        Args:
            score_value (float): The score won in a single match.
        """
        self._tournament_score_value += score_value

    @property
    def tournament_score_value(self) -> float:
        """Reads the total accumulated scores.

        Returns:
            float: The sum of the scores won in every match played.
        """
        return self._tournament_score_value
