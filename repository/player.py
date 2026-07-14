"""Maps a player to and from its stored record."""

from __future__ import annotations

from typing import Any

from models.player import Player


class PlayerJSON:
    """Translates a player between its object form and its stored record."""

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> Player:
        """Builds a player from its stored record.

        Args:
            json_data (dict[str, Any]): The stored record.

        Returns:
            Player: The player.
        """
        return Player(
            pk=json_data["pk"],
            chess_id=json_data["chess_id"],
            last_name=json_data["last_name"],
            first_name=json_data["first_name"],
            birthdate=json_data["birthdate"],
        )

    @staticmethod
    def to_json(player: Player) -> dict[str, Any]:
        """Builds the record of a player.

        Args:
            player (Player): The player to store.

        Returns:
            dict[str, Any]: The record.
        """
        json: dict[str, Any] = {
            "pk": player.pk,
            "chess_id": player.chess_id,
            "last_name": player.last_name,
            "first_name": player.first_name,
            "birthdate": player.birthdate,
        }
        return json
