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


class TournamentRepository(CoreDataRepository[Tournament]):

    def __init__(self) -> None:
        super().__init__(model_class=Tournament)
        self.data_path = TOURNAMENT_DIR
        self.player_registration = PlayerRegistration()

    def get_tournament_by_pk(self, tournament_pk: str) -> Result:
        raw_tournaments: list[dict[str, Any]] = self.read_json_file()
        tournament_result = self.extract_data_by_field(
            raw_data=raw_tournaments,
            field_value=tournament_pk,
        )
        if not tournament_result:
            return tournament_result

        return tournament_result

    def write_registring_player(self, tournament: dict[str, Any]) -> None:
        raw_tournaments = self.read_json_file()
        tournaments_by_pk = self.to_data_by_field_name_dict(
            raw_data=raw_tournaments, field_name="pk"
        )
        tournaments_by_pk[tournament["pk"]] = tournament
        uploaded_tournaments = self.to_data_json(tournaments_by_pk)

        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(uploaded_tournaments, file, indent=4, ensure_ascii=False)

    def register_player_to_tournament(
        self,
        tournament_pk: str,
        chess_id: str,
    ) -> Result:
        tournament_result = self.get_tournament_by_pk(tournament_pk)
        tournament = tournament_result.required_value
        result = self.player_registration.register_player_to_tournament(
            raw_tournament=tournament,
            chess_id=chess_id,
        )
        if not result:
            return result

        self.write_registring_player(result.required_value)
        return result

    def extract_registered_players(
        self,
        registered_players: list[Player],
        registered_chess_ids: list[str],
    ):
        raw_players = self.read_json_file(path=PLAYER_DIR)
        registered_raw_players = self.player_registration.extract_registered_players(
            raw_players=raw_players,
            registered_chess_ids=registered_chess_ids,
        )
        registered_players = self.player_registration.to_players(registered_raw_players)

        return registered_players

    def get_registered_players(self, tournament_pk: str) -> Result:
        tournament_result = self.get_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        registered_players: list[Player] = []
        tournament = tournament_result.required_value

        registered_chess_ids: list[str] = tournament[REGISTERED_PLAYER_CHESS_IDS]
        if not registered_chess_ids:
            return Result.valid(value=registered_players)

        registered_players = self.extract_registered_players(
            registered_players=registered_players,
            registered_chess_ids=registered_chess_ids,
        )

        return Result.valid(value=registered_players)

    def extract_tournament_rounds(self, raw_tournament: dict[str, Any]):
        return raw_tournament["rounds"]

    def get_tournament_rounds(self, tournament_pk: str) -> Result:
        tournament_result = self.get_tournament_by_pk(
            tournament_pk=tournament_pk,
        )
        if not tournament_result:
            return tournament_result

        raw_rounds = self.extract_tournament_rounds(tournament_result.required_value)
        rounds = [Round.from_json(raw_data) for raw_data in raw_rounds]
        return Result.valid(value=rounds)
