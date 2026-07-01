from __future__ import annotations

from typing import Any, TypeAlias
import random

from core.result import Result

from models.tournament import Tournament
from models.round import Round
from models.player import Player
from models.score import PlayerScore

from models.helpers.flat import flat_round_matches, flat_pairs, flat_player_scores
from service.helpers.sort import sort_player_score_by_score

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
        return self.round_not_started(first_round[0])

    def make_pairs(
        self, tournament: Tournament, players: list[Player]
    ) -> list[tuple[Player, Player]]:
        pairs = extract_played_pairs_from_tournament(tournament)

        MAX_TRY_COUNT = len(players) - 1

        picked_up_players: list[Player] = []
        new_pairs: list[tuple[Player, Player]] = []

        for id in range(0, len(players), 2):
            next = 1
            pair = (players[id], players[id + next])
            reversed_pair = (players[id + next], players[id])
            try_count = 0
            while pair in pairs or reversed_pair in pairs or try_count > MAX_TRY_COUNT:
                next += 1
                pair = (players[id], players[id + next])
                reversed_pair = (players[id + next], players[id])
                try_count += 1
            new_pairs.append(pair)
            picked_up_players.append(players[id])
            picked_up_players.append(players[id + next])
        return new_pairs

    def get_sorted_player_scores(self, tournament: Tournament) -> list[PlayerScore]:
        round_matches = flat_round_matches(tournament.rounds)
        player_scores: list[PlayerScore] = flat_player_scores(round_matches)
        sorted_player_scores: list[PlayerScore] = sort_player_score_by_score(
            player_scores
        )
        return sorted_player_scores

    def prepare_players(self, tournament: Tournament) -> list[tuple[Player, Player]]:
        if self.is_first_round(tournament.rounds):
            players = tournament.registered_players
            random.shuffle(players)
            return self.make_pairs(tournament, players)

        sorted_player_scores = self.get_sorted_player_scores(tournament)
        players = extract_player_from_player_scores(sorted_player_scores)
        return self.make_pairs(tournament, players)

    def set_round_players(self, tournament: Tournament, round: Round) -> Result:
        player_pairs_check_result = self.check_registered_players_pairs(tournament)
        if not player_pairs_check_result:
            return player_pairs_check_result

        round.set_round_players(player_pairs=self.prepare_players(tournament))

        return Result.valid(value=tournament)

    def is_even(self, registered_players: list[Player]) -> bool:
        return len(registered_players) % 2 == 0

    def check_registered_players_pairs(self, tournament: Tournament) -> Result:
        if not tournament.registered_players:
            return Result.invalid(reason="No players registered")

        if not self.is_even(tournament.registered_players):
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
