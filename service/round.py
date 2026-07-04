from __future__ import annotations

from typing import Any, TypeAlias
import random

from core.result import Result

from models.tournament import Tournament
from models.round import Round, RoundMatch
from models.player import Player
from models.score import PlayerScore

from models.helpers.flat import flat_round_matches, flat_pairs

Tournaments: TypeAlias = list[Tournament]


def extract_player_from_player_scores(player_scores: list[PlayerScore]) -> list[Player]:
    return [player_score.player for player_score in player_scores]


def extract_played_pairs_from_tournament(
    tournament: Tournament,
) -> list[tuple[Player, Player]]:
    round_matches = flat_round_matches(tournament.rounds)
    pairs = flat_pairs(round_matches)
    return pairs


class RoundService:
    FIRST_ROUND_NAME: str = "round_0"

    def is_first_round(self, rounds: list[Round]):
        first_round = [round for round in rounds if round.name == self.FIRST_ROUND_NAME]
        if not first_round:
            raise ValueError(f"no {self.FIRST_ROUND_NAME} found")

        return self.round_not_started(first_round[0])

    def check_pair(
        self, player_a: Player, player_b: Player, pairs: list[tuple[Player, Player]]
    ) -> bool:
        return bool((player_a, player_b) in pairs or (player_b, player_a) in pairs)

    def make_pairs(
        self, tournament: Tournament, players: list[Player]
    ) -> list[tuple[Player, Player]]:
        pairs = extract_played_pairs_from_tournament(tournament)

        MAX_TRY_COUNT = len(players) - 1

        picked_up_players: list[Player] = []
        new_pairs: list[tuple[Player, Player]] = []

        for id in range(0, len(players)):
            next = 1
            player_a = players[id]
            if player_a in picked_up_players:
                continue

            player_b = players[id + next]
            while player_b in picked_up_players:
                next += 1
                player_b = players[id + next]

            try_count = 0
            while (
                self.check_pair(player_a, player_b, pairs) or try_count > MAX_TRY_COUNT
            ):
                next += 1
                player_b = players[id + next]
                while player_b in picked_up_players:
                    next += 1
                    player_b = players[id + next]

                try_count += 1
            new_pairs.append((player_a, player_b))
            picked_up_players.append(players[id])
            picked_up_players.append(players[id + next])
        return new_pairs

    def prepare_players(
        self, tournament: Tournament, players_by_standing: list[Player]
    ) -> list[tuple[Player, Player]]:
        if self.is_first_round(tournament.rounds):
            players = players_by_standing.copy()
            random.shuffle(players)
            return self.make_pairs(tournament, players)

        return self.make_pairs(tournament, players_by_standing)

    def _set_round_players(
        self, tournament: Tournament, players_by_standing: list[Player], round: Round
    ) -> Result:
        player_pairs_check_result = self.check_registered_players_pairs(
            players_by_standing
        )
        if not player_pairs_check_result:
            return player_pairs_check_result

        round.set_round_players(
            player_pairs=self.prepare_players(tournament, players_by_standing)
        )

        return Result.valid(value=round)

    def is_even(self, registered_players: list[Player]) -> bool:
        return len(registered_players) % 2 == 0

    def check_registered_players_pairs(
        self, players_by_standing: list[Player]
    ) -> Result:
        if not players_by_standing:
            return Result.invalid(reason="No players registered")

        if not self.is_even(players_by_standing):
            return Result.invalid(reason="Odd number of players registered")

        return Result.valid()

    def round_not_started(self, round: Round):
        return not round.round_matches

    def get_next_round(self, tournament_rounds: list[Round]) -> Round | None:
        for round in tournament_rounds:
            round_completed = bool(
                self.are_round_matches_defined(round)
                and not self.incomplete_round_matches_found(
                    self.get_incomplete_round_matches(round)
                )
            )
            if not round_completed:
                return round

        return None

    def extract_tournament_rounds(self, raw_tournament: dict[str, Any]):
        return raw_tournament["rounds"]

    def prepare_next_round(
        self, tournament: Tournament, players_by_standing: list[Player]
    ) -> Result:
        next_round = self.get_next_round(tournament.rounds)
        round_players_result: Result = Result.valid()
        if next_round is None:
            return Result.invalid(reason="no more rounds to run.")

        if not self.are_round_matches_defined(next_round):
            round_players_result = self._set_round_players(
                tournament, players_by_standing, next_round
            )

        if not round_players_result:
            return round_players_result

        return Result.valid(value=next_round)

    def are_round_matches_defined(self, round: Round) -> bool:
        return bool(flat_round_matches([round]))

    def get_incomplete_round_matches(self, round: Round) -> list[RoundMatch]:
        round_matches = flat_round_matches([round])
        incomplete_round_match: list[RoundMatch] = [
            round_match
            for round_match in round_matches
            if round_match.player_score_a.is_score_not_set
            and round_match.player_score_b.is_score_not_set
        ]
        return incomplete_round_match

    def incomplete_round_matches_found(self, incomplete_round_match: list[RoundMatch]):
        return bool(incomplete_round_match)
