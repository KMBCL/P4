"""Orders players and scores."""

from models.player import Player
from models.score import PlayerScore


def sort_players_by_last_name(players: list[Player]) -> list[Player]:
    """Orders players alphabetically, by last name.

    Args:
        players (list[Player]): The players to order.

    Returns:
        list[Player]: The ordered players.
    """
    return sorted(players, key=lambda player: player.last_name)


def sort_player_score_by_score(player_scores: list[PlayerScore]) -> list[PlayerScore]:
    """Orders scores from the highest to the lowest.

    Args:
        player_scores (list[PlayerScore]): The scores to order.

    Returns:
        list[PlayerScore]: The ordered scores.
    """
    return sorted(
        player_scores,
        key=lambda player_score: player_score.score_value,
        reverse=True,
    )


def sort_player_score_by_chess_id(
    player_scores: list[PlayerScore],
) -> list[PlayerScore]:
    """Orders scores by the chess id of their player.

    Args:
        player_scores (list[PlayerScore]): The scores to order.

    Returns:
        list[PlayerScore]: The ordered scores.
    """
    return sorted(
        player_scores,
        key=lambda player_score: player_score.player.chess_id,
    )
