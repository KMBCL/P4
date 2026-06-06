from __future__ import annotations

from typing import Any, TypeAlias
from pathlib import Path
import json

from core.core_data_repository import (
    TOURNAMENT_DIR,
    PLAYER_DIR,
    CoreDataRepository,
)
from controllers.result import Result

from models.tournament import Tournament
from models.round import Round
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

            tournament[REGISTERED_PLAYER_CHESS_IDS].append(chess_id)
            return Result.valid(value=tournaments)

        return Result.invalid(reason=f"Not tournament found with pk : {tournament_pk}")


class TournamentRepository(CoreDataRepository[Tournament]):

    def __init__(self) -> None:
        super().__init__(model_class=Tournament)
        self.data_path = TOURNAMENT_DIR
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

    def get_registered_players(self, tournament_pk: int) -> list[Player]:
        tournaments: list[dict[str, Any]] = self.read_json_file()
        registered_players: list[Player] = []

        for tournament in tournaments:
            if tournament.get("pk") != tournament_pk:
                continue

            registered_chess_ids: list[str] = tournament[REGISTERED_PLAYER_CHESS_IDS]
            if not registered_chess_ids:
                return registered_players

            raw_players = self.read_json_file(path=PLAYER_DIR)

            for raw_player in raw_players:
                chess_id = raw_player["chess_id"]
                if chess_id in registered_chess_ids:
                    player = Player.from_json(raw_player)
                    registered_players.append(player)
                    registered_chess_ids.remove(chess_id)

        return registered_players

    def to_tournament_pks_dict(
        self, raw_tournaments: list[dict[str, Any]]
    ) -> dict[int, dict[str, Any]]:
        tournament_pks: dict[int, dict[str, Any]] = {
            raw_tournament["pk"]: raw_tournament for raw_tournament in raw_tournaments
        }
        return tournament_pks

    def get_tournament_by_pk(self, tournament_pk: int):
        raw_tournaments = self.read_json_file()
        tournaments_by_pks = self.to_tournament_pks_dict(raw_tournaments)

        return tournaments_by_pks.get(tournament_pk, None)

    def extract_tournament_rounds(self, raw_tournament: dict[str, Any]):
        return raw_tournament["rounds"]

    def get_tournament_rounds(self, tournament_pk: int) -> Result:
        raw_tournament = self.get_tournament_by_pk(tournament_pk)
        if raw_tournament is None:
            return Result.invalid(reason="Tournament not found")

        raw_rounds = self.extract_tournament_rounds(raw_tournament)
        rounds = [Round.from_json(raw_data) for raw_data in raw_rounds]
        return Result.valid(value=rounds)
