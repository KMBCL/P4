"""Maps a round and its matches to and from their stored record."""

from __future__ import annotations

from typing import Any

from models.round import Round, RoundMatch


class RoundMatchJSON:
    """Stores a match as the chess id and the score of each of its players."""

    @staticmethod
    def round_match_to_json(round_match: RoundMatch) -> list[list[str]]:
        """Builds the record of a match.

        Args:
            round_match (RoundMatch): The match to store.

        Returns:
            list[list[str]]: The chess id and the score of player a, then of
                player b.
        """
        json: list[list[str]] = [
            [
                round_match.player_score_a.player.chess_id,
                round_match.player_score_a.score,
            ],
            [
                round_match.player_score_b.player.chess_id,
                round_match.player_score_b.score,
            ],
        ]
        return json


class RoundJSON:
    """Translates a round between its object form and its stored record."""

    @staticmethod
    def from_json(json_data: dict[str, Any]) -> Round:
        """Builds a round from its stored record.

        Args:
            json_data (dict[str, Any]): The stored record.

        Returns:
            Round: The round, holding no match object.
        """
        round_matches_payload: list[list[str]] = json_data["round_matches"]
        return Round(
            name=json_data["name"],
            start_timestamp=json_data["start_timestamp"],
            end_timestamp=json_data["end_timestamp"],
            round_matches_payload=round_matches_payload,
        )

    @staticmethod
    def to_json(round: Round) -> dict[str, Any]:
        """Builds the record of a round.

        Args:
            round (Round): The round to store.

        Returns:
            dict[str, Any]: The record, holding every match of the round.
        """
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
