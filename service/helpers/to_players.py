"""Rebuilds players from their stored records."""

from typing import Any

from models.player import Player
from repository.player import PlayerJSON


def to_players(raw_players: list[dict[str, Any]]) -> list[Player]:
    """Rebuilds every player from its stored record.

    Args:
        raw_players (list[dict[str, Any]]): The stored records.

    Returns:
        list[Player]: The players.
    """
    return [PlayerJSON.from_json(raw_player) for raw_player in raw_players]
