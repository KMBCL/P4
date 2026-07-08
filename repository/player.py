from __future__ import annotations

from typing import Any

from models.player import Player


class PlayerJSON:

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> Player:
        return Player(
            pk=json_data["pk"],
            chess_id=json_data["chess_id"],
            last_name=json_data["last_name"],
            first_name=json_data["first_name"],
            birthdate=json_data["birthdate"],
        )

    @staticmethod
    def to_json(player: Player) -> dict[str, Any]:
        json: dict[str, Any] = {
            "pk": player.pk,
            "chess_id": player.chess_id,
            "last_name": player.last_name,
            "first_name": player.first_name,
            "birthdate": player.birthdate,
        }
        return json
