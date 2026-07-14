"""Rebuilds the matches of a round from their stored pairs."""

from repository.repository import Repository

from models.round import RoundMatch, Round
from models.player import Player
from models.score import PlayerScore


class RoundMatchService:
    """Rebuilds the match objects a round only holds as raw pairs."""

    def __init__(self, repository: Repository) -> None:
        """Holds the repository.

        Args:
            repository (Repository): The repository.
        """
        self.repository = repository

    def prepare_players_dict(self, players: list[Player]) -> dict[str, Player]:
        """Indexes the players by their chess id.

        Args:
            players (list[Player]): The players to index.

        Returns:
            dict[str, Player]: The players, keyed by chess id.
        """
        players = players
        players_dict: dict[str, Player] = {
            player.chess_id: player for player in players
        }
        return players_dict

    def build_round_match(
        self, raw_score: list[str], players_dict: dict[str, Player]
    ) -> RoundMatch:
        """Rebuilds one match from the stored chess ids and scores of its players.

        Args:
            raw_score (list[str]): The chess id and the score of each player.
            players_dict (dict[str, Player]): The players, keyed by chess id.

        Returns:
            RoundMatch: The match, holding the score each player took from it.

        Raises:
            ValueError: When a stored chess id matches none of the given players.
        """
        player_a = players_dict.get(raw_score[0][0])
        player_b = players_dict.get(raw_score[1][0])
        if player_a is None or player_b is None:
            raise ValueError("player not found with chess id")

        return RoundMatch(
            player_score_a=PlayerScore(player_a, raw_score[0][1]),
            player_score_b=PlayerScore(player_b, raw_score[1][1]),
        )

    def set_round_matches_from_payload(
        self, players: list[Player], rounds: list[Round]
    ) -> None:
        """Rebuilds the matches of every round, and holds them in it.

        Args:
            players (list[Player]): The players registered to the tournament.
            rounds (list[Round]): The rounds to rebuild the matches of.
        """
        players_dict = self.prepare_players_dict(players)
        for round in rounds:
            round_matches: list[RoundMatch] = [
                self.build_round_match(raw_score, players_dict)
                for raw_score in round.round_matches_payload
            ]
            round.set_round_matches_from_payload(round_matches)
