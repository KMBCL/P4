from __future__ import annotations

from typing import Any, TypeAlias
from pathlib import Path
import json

from core.core_data_repository import (
    DATA_BASE_ROOT,
    CoreDataRepository,
)
from controllers.result import Result

from models.tournament import Tournament

Tournaments: TypeAlias = list[Tournament]


class PlayerRegistration:
    REGISTERED_PLAYER_CHESS_IDS = "registered_player_chess_ids"

    def ensure_registered_player_chess_ids_field(
        self,
        tournament: dict[str, Any],
    ) -> dict[str, Any]:
        registered_player_chess_ids: list[str] = []

        if self.REGISTERED_PLAYER_CHESS_IDS not in tournament:
            tournament[self.REGISTERED_PLAYER_CHESS_IDS] = registered_player_chess_ids

        return tournament

    def check_if_player_already_registered(
        self,
        chess_id: str,
        tournament: dict[str, Any],
    ) -> Result:
        if chess_id in tournament[self.REGISTERED_PLAYER_CHESS_IDS]:
            return Result.invalid(
                reason=f"Player with chess_id : {chess_id} is already registered"
            )

        return Result.valid()

    def register_player_to_tournament(
        self,
        tournaments: list[dict[str, Any]],
        tournament_pk: int,
        chess_id: str,
    ) -> Result:

        for tournament in tournaments:
            if tournament.get("pk") != tournament_pk:
                continue

            tournament = self.ensure_registered_player_chess_ids_field(tournament)
            already_registered_result = self.check_if_player_already_registered(
                chess_id=chess_id,
                tournament=tournament,
            )
            if not already_registered_result:
                return already_registered_result

            tournament[self.REGISTERED_PLAYER_CHESS_IDS].append(chess_id)
            return Result.valid(value=tournaments)

        return Result.invalid(reason=f"Not tournament found with pk : {tournament_pk}")


class TournamentRepository(CoreDataRepository[Tournament]):

    def __init__(self) -> None:
        super().__init__(model_class=Tournament)
        self.data_path = Path(f"{DATA_BASE_ROOT}/tournaments.json")
        self.player_registration = PlayerRegistration()

    def register_player_to_tournament(
        self,
        tournament_pk: int,
        chess_id: str,
    ) -> Result:
        tournaments: list[dict[str, Any]] = self.read_json_file()

        result = self.player_registration.register_player_to_tournament(
            tournaments=tournaments,
            tournament_pk=tournament_pk,
            chess_id=chess_id,
        )
        if not result:
            return result

        updated_tournaments = result.required_value

        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(updated_tournaments, file, indent=4, ensure_ascii=False)

        return result
