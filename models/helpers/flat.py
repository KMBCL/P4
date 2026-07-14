"""Flattens the nested rounds, matches and scores of a tournament."""

from models.round import Round, RoundMatch
from models.score import PlayerScore
from models.player import Player


def flat_round_matches(rounds: list[Round]) -> list[RoundMatch]:
    """Collects the matches of every round.

    Args:
        rounds (list[Round]): The rounds to walk.

    Returns:
        list[RoundMatch]: Every match, in the order its round was played.
    """
    return [round_match for round in rounds for round_match in round.round_matches]


def flat_player_scores(round_matches: list[RoundMatch]) -> list[PlayerScore]:
    """Collects the two scores of every match.

    Args:
        round_matches (list[RoundMatch]): The matches to walk.

    Returns:
        list[PlayerScore]: Every score, of which a player holds as many as the
            matches they played.
    """
    return [
        player_score
        for round_match in round_matches
        for player_score in round_match.to_list()
    ]


def flat_pairs(round_matches: list[RoundMatch]) -> list[tuple[Player, Player]]:
    """Collects the two players opposed by every match.

    Args:
        round_matches (list[RoundMatch]): The matches to walk.

    Returns:
        list[tuple[Player, Player]]: Every pair, as opposed by the match and not
            in any normalised order.
    """
    return [
        (
            round_match.player_score_a.player,
            round_match.player_score_b.player,
        )
        for round_match in round_matches
    ]
