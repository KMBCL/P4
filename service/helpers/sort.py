from models.player import Player
from models.score import PlayerScore


def sort_players_by_last_name(players: list[Player]) -> list[Player]:
    return sorted(players, key=lambda player: player.last_name)


def sort_player_score_by_score(player_scores: list[PlayerScore]) -> list[PlayerScore]:
    return sorted(
        player_scores,
        key=lambda player_score: player_score.score_value,
        reverse=True,
    )


def sort_player_score_by_chess_id(
    player_scores: list[PlayerScore],
) -> list[PlayerScore]:
    return sorted(
        player_scores,
        key=lambda player_score: player_score.player.chess_id,
    )
