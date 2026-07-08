from __future__ import annotations

from typing import Any

from models.tournament import Tournament
from repository.round import RoundJSON
from repository.player_registry import PlayerRegistrationJSON


class TournamentJSON:

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> Tournament:
        return Tournament(
            pk=json_data["pk"],
            name=json_data["name"],
            place=json_data["place"],
            start_date=json_data["start_date"],
            end_date=json_data["end_date"],
            description=json_data["description"],
            player_count=len(json_data["registered_player_chess_ids"]),
            round_count=json_data["round_count"],
            registered_player_payload=json_data["registered_player_chess_ids"],
            rounds=[RoundJSON.from_json(data) for data in json_data["rounds"]],
        )

    @staticmethod
    def to_json(tournament: Tournament) -> dict[str, Any]:
        json: dict[str, Any] = {
            "pk": tournament.pk,
            "name": tournament.name,
            "place": tournament.place,
            "start_date": tournament.start_date,
            "end_date": tournament.end_date,
            "description": tournament.description,
            "round_count": tournament.round_count,
            "registered_player_chess_ids": [
                PlayerRegistrationJSON.to_json(player)
                for player in tournament.registered_players
            ],
            "rounds": [RoundJSON.to_json(round) for round in tournament.rounds],
        }
        return json
