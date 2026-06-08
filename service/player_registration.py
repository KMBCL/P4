from __future__ import annotations

from typing import Any, TypeAlias
from itertools import combinations
import random
import json

from core.core_data_repository import (
    TOURNAMENT_DIR,
    PLAYER_DIR,
    CoreDataRepository,
)
from controllers.result import Result

from models.tournament import Tournament
from models.round import Round, RoundMatch
from models.player import Player

Tournaments: TypeAlias = list[Tournament]

REGISTERED_PLAYER_CHESS_IDS = "registered_player_chess_ids"


class PlayerRegistration:

    def ensure_registered_player_chess_ids_field(
        self,
        tournament: dict[str, Any],
    ) -> dict[str, Any]:
        registered_player_chess_ids: list[str] = []

        if REGISTERED_PLAYER_CHESS_IDS not in tournament:
            tournament[REGISTERED_PLAYER_CHESS_IDS] = registered_player_chess_ids

        return tournament

    def check_if_player_already_registered(
        self,
        chess_id: str,
        tournament: dict[str, Any],
    ) -> Result:
        if chess_id in tournament[REGISTERED_PLAYER_CHESS_IDS]:
            return Result.invalid(
                reason=f"Player with chess_id : {chess_id} is already registered"
            )

        return Result.valid()

    def register_player_to_tournament(
        self,
        raw_tournament: dict[str, Any],
        chess_id: str,
    ) -> Result:
        tournament = self.ensure_registered_player_chess_ids_field(raw_tournament)
        already_registered_result = self.check_if_player_already_registered(
            chess_id=chess_id,
            tournament=tournament,
        )
        if not already_registered_result:
            return already_registered_result

        tournament[REGISTERED_PLAYER_CHESS_IDS].append(chess_id)
        return Result.valid(value=raw_tournament)

    def extract_registered_players(
        self,
        raw_players: list[dict[str, Any]],
        registered_chess_ids: list[str],
    ) -> list[dict[str, Any]]:
        raw_registered_players = [
            raw_player
            for raw_player in raw_players
            if raw_player["chess_id"] in registered_chess_ids
        ]
        return raw_registered_players

    def to_players(self, registered_raw_players: list[dict[str, Any]]) -> list[Player]:
        players = [
            Player.from_json(raw_player) for raw_player in registered_raw_players
        ]
        return players
