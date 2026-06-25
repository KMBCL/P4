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

from models.tournament import Tournament
from models.round import Round, RoundMatch
from models.player import Player

Tournaments: TypeAlias = list[Tournament]

REGISTERED_PLAYER_CHESS_IDS = "registered_player_chess_ids"


class RoundHandler:
    FIRST_ROUND_NAME: str = "round_0"

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

    def prepare_chess_ids(self, tournament: Tournament) -> list[str]:
        if self.is_first_round(tournament.rounds):
            chess_ids = tournament.registered_player_chess_ids
            random.shuffle(chess_ids)
            return chess_ids

        sorted_players = tournament.get_player_scores()
        chess_ids: list[str] = [chess_id for chess_id, _ in sorted_players.items()]
        return chess_ids

    def make_player_pairs(
        self,
        tournament: Tournament,
    ) -> list[tuple[str, str]]:
        chess_ids: list[str] = self.prepare_chess_ids(tournament)
        pairs = self.make_pairs(chess_ids)
        return pairs

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

    def set_round_players(self, tournament: Tournament, round: Round) -> Result:
        player_pairs_check_result = self.check_registered_players_pairs(tournament)
        if not player_pairs_check_result:
            return player_pairs_check_result

        shuffled_pairs: list[tuple[str, str]] = self.make_player_pairs(tournament)
        round.set_round_players(player_pairs=shuffled_pairs)

        return Result.valid(value=tournament)
