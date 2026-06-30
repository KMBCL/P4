from __future__ import annotations

from typing import Any, TypeAlias
import random

from core.result import Result

from models.tournament import Tournament
from models.round import Round

from models.helpers.flat import flat_rounds, flat_scores, flat_pairs

Tournaments: TypeAlias = list[Tournament]

REGISTERED_PLAYER_CHESS_IDS = "registered_player_chess_ids"


def swap_next(id: int, reordered_list: list[str]) -> None:
    reordered_list[id + 1], reordered_list[id + 2] = (
        reordered_list[id + 2],
        reordered_list[id + 1],
    )


def swap_previous(id: int, reordered_list: list[str]) -> None:
    reordered_list[id - 1], reordered_list[id] = (
        reordered_list[id],
        reordered_list[id - 1],
    )


def sort_player_scores(player_scores: dict[str, float]) -> dict[str, float]:
    return dict(
        sorted(
            player_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


class RoundService:
    FIRST_ROUND_NAME: str = "round_0"

    def is_first_round(self, rounds: list[Round]):
        first_round = [round for round in rounds if round.name == self.FIRST_ROUND_NAME]
        return self.round_not_started(first_round[0])

    def reorder_if_played(self, tournament: Tournament, chess_ids: list[str]) -> Result:
        round_matches = flat_rounds(tournament.rounds)
        pairs = flat_pairs(round_matches)

        MAX_TRY_COUNT = len(chess_ids) - 1
        reordered_list: list[str] = chess_ids.copy()

        for id in range(0, len(reordered_list), 2):
            pair = set((reordered_list[id], reordered_list[id + 1]))
            try_count = 0
            while pair in pairs:

                try:
                    swap_next(id, reordered_list)
                except IndexError:
                    swap_previous(id, reordered_list)

                pair = (reordered_list[id], reordered_list[id + 1])
                try_count += 1

                if try_count > MAX_TRY_COUNT:
                    return Result.invalid(
                        reason=f"Unable to make new pair for player {id}"
                    )

        return Result.valid(reordered_list)

    def get_player_scores(self, tournament: Tournament) -> dict[str, float]:
        player_scores: dict[str, float] = {}
        round_matches = flat_rounds(tournament.rounds)
        scores = flat_scores(round_matches)
        for score in scores:
            if player_scores.get(score.chess_id, None) is None:
                player_scores[score.chess_id] = score.score_value
                continue

            player_scores[score.chess_id] += score.score_value

        return player_scores

    def prepare_chess_ids(self, tournament: Tournament) -> Result:
        if self.is_first_round(tournament.rounds):
            chess_ids = tournament.registered_player_chess_ids
            random.shuffle(chess_ids)
            return Result.valid(chess_ids)

        player_scores = self.get_player_scores(tournament)
        sorted_scores = sort_player_scores(player_scores)
        chess_ids: list[str] = [chess_id for chess_id, _ in sorted_scores.items()]

        return self.reorder_if_played(tournament, chess_ids)

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
    ) -> Result:
        chess_id_result = self.prepare_chess_ids(tournament)
        if not chess_id_result:
            return chess_id_result

        chess_ids: list[str] = chess_id_result.get_value()
        pairs = self.make_pairs(chess_ids)
        return Result.valid(pairs)

    def set_round_players(self, tournament: Tournament, round: Round) -> Result:
        player_pairs_check_result = self.check_registered_players_pairs(tournament)
        if not player_pairs_check_result:
            return player_pairs_check_result

        shuffled_pairs_result = self.make_player_pairs(tournament)
        if not shuffled_pairs_result:
            return shuffled_pairs_result

        shuffled_pairs: list[tuple[str, str]] = shuffled_pairs_result.get_value()
        round.set_round_players(player_pairs=shuffled_pairs)

        return Result.valid(value=tournament)

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

    def get_next_round(self, tournament_rounds: list[Round]) -> Round | None:
        for round in tournament_rounds:
            round_completed = bool(
                round.are_round_matches_defined() and round.is_round_score_complete()
            )
            if not round_completed:
                return round

        return None

    def extract_tournament_rounds(self, raw_tournament: dict[str, Any]):
        return raw_tournament["rounds"]

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
