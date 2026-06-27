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
from core.result import Result
from service.tournament import TournamentService
from service.round import RoundService

from models.tournament import Tournament
from models.round import Round, RoundMatch
from models.player import Player

Tournaments: TypeAlias = list[Tournament]


class RoundController:

    def __init__(
        self, service: RoundService, tournament_service: TournamentService
    ) -> None:
        self.service = service
        self.tournament_service = tournament_service

    def make_pairs(self, chess_ids: list[str]) -> list[tuple[str, str]]:
        PAIR_LENGTH = 2
        pairs: list[tuple[str, str]] = []
        pair: list[str] = []
        for chess_id in chess_ids:
            pair.append(chess_id)
            if len(pair) == PAIR_LENGTH:
                pairs.append(
                    (
                        pair[0],
                        pair[1],
                    )
                )
                pair = []
        return pairs

    def make_player_pairs(
        self,
        tournament: Tournament,
    ) -> list[tuple[str, str]]:
        chess_ids: list[str] = self.service.prepare_chess_ids(tournament)
        pairs = self.make_pairs(chess_ids)
        return pairs

    def set_round_players(self, tournament: Tournament, round: Round) -> Result:
        player_pairs_check_result = self.service.check_registered_players_pairs(
            tournament
        )
        if not player_pairs_check_result:
            return player_pairs_check_result

        shuffled_pairs: list[tuple[str, str]] = self.make_player_pairs(tournament)
        round.set_round_players(player_pairs=shuffled_pairs)

        return Result.valid(value=tournament)

    def save_round_players(self, tournament: Tournament, round: Round) -> Result:
        tournament_result = self.set_round_players(tournament=tournament, round=round)
        self.tournament_service.save_tournament(tournament)
        return tournament_result

    def extract_tournament_rounds(self, raw_tournament: dict[str, Any]):
        return raw_tournament["rounds"]

    def get_tournament_rounds(self, tournament_pk: str) -> Result:
        tournament_result = self.tournament_service.get_raw_tournament_by_pk(
            tournament_pk
        )
        if not tournament_result:
            return tournament_result

        raw_rounds = self.extract_tournament_rounds(tournament_result.get_result())
        rounds = [Round.from_json(raw_data) for raw_data in raw_rounds]
        return Result.valid(value=rounds)

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
