from __future__ import annotations

from typing import Any

from models.round import Round, RoundMatch


class RoundMatchJSON:

    @staticmethod
    def round_match_to_json(round_match: RoundMatch) -> list[list[str]]:
        json: list[list[str]] = [
            [
                round_match.player_score_a.player.chess_id,
                round_match.player_score_a.score,
            ],
            [
                round_match.player_score_a.player.chess_id,
                round_match.player_score_a.score,
            ],
        ]
        return json


class RoundJSON:

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> Round:
        round_matches_payload: list[list[str]] = json_data["round_matches"]
        return Round(
            name=json_data["name"],
            start_timestamp=json_data["start_timestamp"],
            end_timestamp=json_data["end_timestamp"],
            round_matches_payload=round_matches_payload,
        )

    @staticmethod
    def to_json(round: Round) -> dict[str, Any]:
        json: dict[str, Any] = {
            "name": round.name,
            "start_timestamp": round.start_timestamp,
            "end_timestamp": round.end_timestamp,
            "round_matches": [
                RoundMatchJSON.round_match_to_json(round_match)
                for round_match in round.round_matches
            ],
        }
        return json
