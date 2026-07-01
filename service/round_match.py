from repository.repository import Repository
from repository.paths import PLAYER_DIR


from models.round import RoundMatch, Round
from models.player import Player
from models.score import PlayerScore

from service.helpers.to_players import to_players


class RoundMatchService:

    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def prepare_players_dict(self, players: list[Player]) -> dict[str, Player]:
        players = players
        players_dict: dict[str, Player] = {
            player.chess_id: player for player in players
        }
        return players_dict

    def build_round_match(
        self, raw_score: list[str], players_dict: dict[str, Player]
    ) -> RoundMatch:
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
        players_dict = self.prepare_players_dict(players)
        for round in rounds:
            round_matches: list[RoundMatch] = [
                self.build_round_match(raw_score, players_dict)
                for raw_score in round.round_matches_payload
            ]
            round.set_round_matches_from_payload(round_matches)
