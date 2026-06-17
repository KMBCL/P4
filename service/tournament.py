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

    def check_chess_id_exists(self, chess_id: str) -> Result:
        if not self.player_registration.validate_chess_id_exists(
            chess_id, self.repository.read_json_file(path=PLAYER_DIR)
        ):
            return Result.invalid(
                reason=f"Player with this chess ID : {chess_id} doesn't exists in database"
            )

        return Result.valid()

    def check_tournament_is_begun(self, tournament_pk: str) -> Result:
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        tournament: Tournament = Tournament.from_json(tournament_result.required_value)
        if tournament.has_begun:
            return Result.invalid(
                reason="Tournament is already begun, cannot add new players"
            )

        return Result.valid()

    def register_player_to_tournament(
        self,
        tournament_pk: str,
        chess_id: str,
    ) -> Result:
        chess_id_result = self.check_chess_id_exists(chess_id)
        if not chess_id_result:
            return chess_id_result

        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        # has_begun_result = self.check_tournament_is_begun(
        #     tournament_result.required_value
        # )
        # if not has_begun_result:
        #     return has_begun_result

        raw_tournament = tournament_result.required_value
        result = self.player_registration.register_player_to_tournament(
            raw_tournament=raw_tournament,
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

    def get_next_round(self, tournament_rounds: list[Round]) -> Round | None:
        for round in tournament_rounds:
            round_completed = bool(
                round.are_round_matches_defined() and round.is_round_score_complete()
            )
            if not round_completed:
                return round

        return None

    def set_round_players(self, tournament: Tournament, round: Round) -> Result:
        round_handler = RoundHandler()
        tournament_result = round_handler.set_round_players(
            tournament=tournament, round=round
        )
        self.save_tournament(tournament)
        return tournament_result

    def save_tournament(self, tournament: Tournament) -> None:
        tournament_json = tournament.to_json()
        uploaded_tournaments = self.repository.update_model_json(tournament_json)
        self.repository.write_json_data(uploaded_tournaments)

    def set_round_matches(self, tournament: Tournament, round: Round) -> Result:
        tournament_result = self.set_round_players(tournament, round)
        if not tournament_result:
            return tournament_result

        tournament = tournament_result.required_value
        self.save_tournament(tournament)
        return Result.valid(value=round)

    def extract_incomplete_matches(self, round: Round) -> list[RoundMatch]:
        incomplete_scores: list[RoundMatch] = []
        if not round.is_round_score_complete():
            incomplete_scores = [
                round_match
                for round_match in round.round_matches
                if not round_match.is_score_complete()
            ]
        return incomplete_scores

    def prepare_next_round(self, tournament: Tournament) -> Result:
        next_round = self.get_next_round(tournament.rounds)
        round_players_result: Result = Result.valid()
        if next_round is None:
            return Result.invalid(reason="no more rounds to run.")

        if not next_round.are_round_matches_defined():
            round_players_result = self.set_round_players(tournament, next_round)

        if not round_players_result:
            return round_players_result

        return Result.valid(value=next_round)
