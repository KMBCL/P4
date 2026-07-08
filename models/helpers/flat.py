from models.round import Round, RoundMatch
from models.score import PlayerScore
from models.player import Player


def flat_round_matches(rounds: list[Round]) -> list[RoundMatch]:
    return [round_match for round in rounds for round_match in round.round_matches]


def flat_player_scores(round_matches: list[RoundMatch]) -> list[PlayerScore]:
    return [
        player_score
        for round_match in round_matches
        for player_score in round_match.to_list()
    ]


def flat_pairs(round_matches: list[RoundMatch]) -> list[tuple[Player, Player]]:
    return [
        (
            round_match.player_score_a.player,
            round_match.player_score_b.player,
        )
        for round_match in round_matches
    ]
