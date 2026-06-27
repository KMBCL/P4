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

from models.tournament import Tournament
from models.round import Round, RoundMatch
from models.player import Player

Tournaments: TypeAlias = list[Tournament]

REGISTERED_PLAYER_CHESS_IDS = "registered_player_chess_ids"


class RoundService:
    FIRST_ROUND_NAME: str = "round_0"

    def prepare_chess_ids(self, tournament: Tournament) -> list[str]:
        if self.is_first_round(tournament.rounds):
            chess_ids = tournament.registered_player_chess_ids
            random.shuffle(chess_ids)
            return chess_ids

        sorted_players = tournament.get_player_scores()
        chess_ids: list[str] = [chess_id for chess_id, _ in sorted_players.items()]
        return chess_ids

    def is_even(self, registered_player_chess_ids: list[str]) -> bool:
        return len(registered_player_chess_ids) % 2 == 0

    def check_registered_players_pairs(self, tournament: Tournament) -> Result:
        if not tournament.registered_player_chess_ids:
            return Result.invalid(reason="No players registered")

        if not self.is_even(tournament.registered_player_chess_ids):
            return Result.invalid(reason="Odd number of players registered")

        return Result.valid()

    def round_not_started(self, round: Round):
        return not round.round_matches

    def is_first_round(self, rounds: list[Round]):
        first_round = [round for round in rounds if round.name == self.FIRST_ROUND_NAME]
        return self.round_not_started(first_round[0])

    def get_next_round(self, tournament_rounds: list[Round]) -> Round | None:
        for round in tournament_rounds:
            round_completed = bool(
                round.are_round_matches_defined() and round.is_round_score_complete()
            )
            if not round_completed:
                return round

        return None

    def extract_incomplete_matches(self, round: Round) -> list[RoundMatch]:
        incomplete_scores: list[RoundMatch] = []
        if not round.is_round_score_complete():
            incomplete_scores = [
                round_match
                for round_match in round.round_matches
                if not round_match.is_score_complete()
            ]
        return incomplete_scores
