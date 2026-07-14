"""Provides the round and match domain models, and the scores a match awards."""

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
    """Opposes two players, and holds the score each one took from the match."""

    player_score_a: PlayerScore
    player_score_b: PlayerScore

    def set_draw(self):
        """Awards the draw score to both players."""
        self.player_score_a.score_value = DRAW_SCORE
        self.player_score_b.score_value = DRAW_SCORE

    def _set_score(self, player_score: PlayerScore, winner: Player) -> None:
        """Awards one player the victory or the defeat score.

        Args:
            player_score (PlayerScore): The score to write.
            winner (Player): The player who won the match, compared by chess id.
        """
        if player_score.player.chess_id == winner.chess_id:
            player_score.score_value = VICTORY_SCORE
        else:
            player_score.score_value = DEFEAT_SCORE

    def set_score(self, winner: Player | None) -> None:
        """Awards the scores of the match to both players.

        Args:
            winner (Player | None): The player who won, or None for a draw.
        """
        if winner is None:
            self.set_draw()
            return None

        self._set_score(self.player_score_a, winner)
        self._set_score(self.player_score_b, winner)

    def to_list(self) -> list[PlayerScore]:
        """Exposes both player scores as a list.

        Returns:
            list[PlayerScore]: The scores of player a and player b, in that order.
        """
        return [self.player_score_a, self.player_score_b]


def default_matches() -> list[RoundMatch]:
    """Builds the default matches of a round.

    Returns:
        list[RoundMatch]: An empty list.
    """
    return []


def default_raw_matches() -> list[list[str]]:
    """Builds the default raw matches of a round.

    Returns:
        list[list[str]]: An empty list.
    """
    return []


@dataclass
class Round(Model[Any]):
    """Groups the matches played by every registered player."""

    name: str
    start_timestamp: str
    end_timestamp: str
    round_matches_payload: list[list[str]] = field(default_factory=default_raw_matches)
    round_matches: list[RoundMatch] = field(default_factory=default_matches)

    def set_round_players(self, player_pairs: list[tuple[Player, Player]]) -> None:
        """Pairs the players of the round, and opens a match for each pair.

        Every match starts with both scores unset.

        Args:
            player_pairs (list[tuple[Player, Player]]): The players to oppose.
        """
        round_matches: list[RoundMatch] = [
            RoundMatch(
                player_score_a=PlayerScore(player=player_a),
                player_score_b=PlayerScore(player=player_b),
            )
            for player_a, player_b in player_pairs
        ]
        self.round_matches = round_matches

    def set_round_matches_from_payload(self, round_matches: list[RoundMatch]) -> None:
        """Holds the matches rebuilt from the raw pairs read from storage.

        Args:
            round_matches (list[RoundMatch]): The matches rebuilt by the caller.
        """
        self.round_matches = round_matches
