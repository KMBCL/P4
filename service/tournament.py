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

from service.player_registration import PlayerRegistration
from service.round import RoundHandler


class TournamentService:

    def __init__(self) -> None:

        self.repository = CoreDataRepository[Tournament](Tournament)
        self.repository.data_path = TOURNAMENT_DIR
        self.player_registration = PlayerRegistration()

    def get_raw_tournament_by_pk(self, tournament_pk: str) -> Result:
        raw_tournaments: list[dict[str, Any]] = self.repository.read_json_file()
        tournament_result = self.repository.extract_data_by_field(
            raw_data=raw_tournaments,
            field_value=tournament_pk,
        )
        if not tournament_result:
            return tournament_result

        return tournament_result

    def get_tournament_by_pk(self, tournament_pk: str) -> Result:
        raw_tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not raw_tournament_result:
            return raw_tournament_result

        return Result.valid(
            value=Tournament.from_json(raw_tournament_result.required_value)
        )

    def register_player_to_tournament(
        self,
        tournament_pk: str,
        chess_id: str,
    ) -> Result:
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        tournament = tournament_result.required_value
        result = self.player_registration.register_player_to_tournament(
            raw_tournament=tournament,
            chess_id=chess_id,
        )
        if not result:
            return result

        self.repository.update_model(result.required_value)
        return result

    def extract_registered_players(
        self,
        registered_players: list[Player],
        registered_chess_ids: list[str],
    ):
        raw_players = self.repository.read_json_file(path=PLAYER_DIR)
        registered_raw_players = self.player_registration.extract_registered_players(
            raw_players=raw_players,
            registered_chess_ids=registered_chess_ids,
        )
        registered_players = self.player_registration.to_players(registered_raw_players)

        return registered_players

    def get_registered_players(self, tournament_pk: str) -> Result:
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
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
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        raw_rounds = self.extract_tournament_rounds(tournament_result.required_value)
        rounds = [Round.from_json(raw_data) for raw_data in raw_rounds]
        return Result.valid(value=rounds)

    def set_round_matches(self, tournament_pk: str, round_name: str) -> Result:
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        tournament: Tournament = Tournament.from_json(tournament_result.required_value)
        round_handler = RoundHandler()
        tournament_result = round_handler.set_round_players(
            tournament=tournament, round_name=round_name
        )
        if not tournament_result:
            return tournament_result

        tournament = tournament_result.required_value
        tournament_json = tournament.to_json()
        uploaded_tournaments = self.repository.update_model_json(tournament_json)
        self.repository.write_json_data(uploaded_tournaments)
        return Result.valid(value=tournament.get_round(round_name=round_name))

    def get_round_matches(self, tournament_pk: str, round_name: str) -> Result:
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        tournament = Tournament.from_json(tournament_result.required_value)
        round = tournament.get_round(round_name)
        if round is None:
            return Result.invalid(reason="Round not found")

        return Result.valid(value=round.round_matches)

    def save_round_matches(
        self, round_matches: list[RoundMatch], tournament_pk: str, round_name: str
    ):
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        tournament = Tournament.from_json(tournament_result.required_value)
        round = tournament.get_round(round_name)
        if round is None:
            return Result.invalid(reason="Round not found")

        tournament.update_round_matches(round_matches, round_name)
        tournament_json = tournament.to_json()
        self.repository.update_model(tournament_json)
