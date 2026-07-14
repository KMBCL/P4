"""Applies the rules governing the rounds, and pairs the players of each one."""

from __future__ import annotations

from dataclasses import dataclass

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
    """Gats the player of every score.

    Args:
        player_scores (list[PlayerScore]): The scores to read.

    Returns:
        list[Player]: The players.
    """
    return [player_score.player for player_score in player_scores]


def extract_played_pairs_from_tournament(
    tournament: Tournament,
) -> list[tuple[Player, Player]]:
    """Collects every pair the tournament has already opposed.

    Args:
        tournament (Tournament): The tournament to walk.

    Returns:
        list[tuple[Player, Player]]: The pairs, of every match of every round.
    """
    round_matches = flat_round_matches(tournament.rounds)
    pairs = flat_pairs(round_matches)
    return pairs


@dataclass
class PairHelper:
    """Pairs players, avoiding a rematch as long as one can be avoided."""

    players: list[Player]
    played_pairs: list[tuple[Player, Player]]

    def _pair_already_played(
        self,
        player_a: Player,
        player_b: Player,
    ) -> bool:
        """Tells if two players have already met.

        Both orders are compared, as a pair is not stored in any given order.

        Args:
            player_a (Player): The first player.
            player_b (Player): The second player.

        Returns:
            bool: True when the two players have already met.
        """
        return bool(
            (player_a, player_b) in self.played_pairs
            or (player_b, player_a) in self.played_pairs
        )

    def _pick_opponent(
        self, player_a: Player, remaining_players: list[Player]
    ) -> Player:
        """Picks the first player that has not met the given one yet.

        A rematch is accepted as a last resort: when every remaining player has
        already met the given one, the first remaining player is picked.

        Args:
            player_a (Player): The player to find an opponent to.
            remaining_players (list[Player]): The players left to pair.

        Returns:
            Player: The opponent.
        """
        for remaining_player in remaining_players:
            if self._pair_already_played(player_a, remaining_player):
                continue

            return remaining_player

        return remaining_players[0]

    def build_new_pairs(self) -> list[tuple[Player, Player]]:
        """Pairs every player, taking them in the order they are given.

        Returns:
            list[tuple[Player, Player]]: The new pairs.
        """
        new_pairs: list[tuple[Player, Player]] = []
        remaining_players = self.players.copy()
        while remaining_players:

            player_a = remaining_players[0]
            remaining_players.remove(player_a)

            player_b = self._pick_opponent(player_a, remaining_players)
            remaining_players.remove(player_b)

            new_pairs.append((player_a, player_b))

        return new_pairs


class RoundService:
    """Runs the rounds of a tournament, one after the other."""

    def is_first_round(self, rounds: list[Round]):
        """Tells if the tournament has yet to play its first round.

        Args:
            rounds (list[Round]): The rounds of the tournament.

        Returns:
            bool: True when the first round holds no match yet.
        """
        return self.round_not_started(rounds[0])

    def make_pairs(
        self, tournament: Tournament, players: list[Player]
    ) -> list[tuple[Player, Player]]:
        """Pairs the players, against the pairs the tournament already opposed.

        Args:
            tournament (Tournament): The tournament holding the played pairs.
            players (list[Player]): The players to pair, in the order to pair them.

        Returns:
            list[tuple[Player, Player]]: The new pairs.
        """
        pairs = extract_played_pairs_from_tournament(tournament)
        pair_helper = PairHelper(players, pairs)
        new_pairs = pair_helper.build_new_pairs()
        return new_pairs

    def prepare_players(
        self, tournament: Tournament, players_by_standing: list[Player]
    ) -> list[tuple[Player, Player]]:
        """Pairs the players of the round to come.

        The first round is drawn at random. Every later round pairs the players
        by standing.

        Args:
            tournament (Tournament): The tournament to pair the players of.
            players_by_standing (list[Player]): The players, best standing first.

        Returns:
            list[tuple[Player, Player]]: The new pairs.
        """
        if self.is_first_round(tournament.rounds):
            players = players_by_standing.copy()
            random.shuffle(players)
            return self.make_pairs(tournament, players)

        return self.make_pairs(tournament, players_by_standing)

    def _set_round_players(
        self, tournament: Tournament, players_by_standing: list[Player], round: Round
    ) -> Result:
        """Pairs the players, and opens the matches of the round.

        Args:
            tournament (Tournament): The tournament the round belongs to.
            players_by_standing (list[Player]): The players, best standing first.
            round (Round): The round to open the matches of.

        Returns:
            Result:
                - A valid result carrying the round, matches opened.
                - An invalid one when the players cannot be paired.
        """
        player_pairs_check_result = self.check_registered_players_pairs(
            players_by_standing
        )
        if not player_pairs_check_result.is_valid():
            return player_pairs_check_result

        round.set_round_players(
            player_pairs=self.prepare_players(tournament, players_by_standing)
        )

        return Result.valid(value=round)

    def is_even(self, registered_players: list[Player]) -> bool:
        """Tells if the players can all be paired.

        Args:
            registered_players (list[Player]): The players to pair.

        Returns:
            bool: True when the players are in an even number.
        """
        return len(registered_players) % 2 == 0

    def check_registered_players_pairs(
        self, players_by_standing: list[Player]
    ) -> Result:
        """Tells if the registered players can be paired.

        The valid result carries no value: it is read with is_valid only. Gate mode.


        Args:
            players_by_standing (list[Player]): The players to pair.

        Returns:
            Result:
                - A valid result, holding no value, when the players can be paired.
                - An invalid one when no player is registered, or when they are
                  in an odd number.
        """
        if not players_by_standing:
            return Result.invalid(reason="No players registered")

        if not self.is_even(players_by_standing):
            return Result.invalid(reason="Odd number of players registered")

        return Result.valid()

    def round_not_started(self, round: Round):
        """Tells if the round has yet to be paired.

        Args:
            round (Round): The round to read.

        Returns:
            bool: True when the round holds no match.
        """
        return not round.round_matches

    def get_next_round(self, tournament_rounds: list[Round]) -> Round | None:
        """Reads the first round that is not completed.

        A round is completed once its matches are opened and every one of them
        holds a score.

        Args:
            tournament_rounds (list[Round]): The rounds of the tournament.

        Returns:
            Round | None: The round to run, or None when every round is completed.
        """
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
        """Reads the rounds of a stored tournament.

        Args:
            raw_tournament (dict[str, Any]): The stored record of the tournament.

        Returns:
            list[dict[str, Any]]: The stored records of its rounds.
        """
        return raw_tournament["rounds"]

    def prepare_next_round(
        self, tournament: Tournament, players_by_standing: list[Player]
    ) -> Result:
        """Reads the round to run, and pairs its players when it has none yet.

        A round that is already paired is returned untouched, so that a
        tournament resumed from storage keeps the pairs it was left with.

        Args:
            tournament (Tournament): The tournament to run.
            players_by_standing (list[Player]): The players, best standing first.

        Returns:
            Result:
                - A valid result carrying the round to run.
                - An invalid one when every round is completed, or when the
                  players cannot be paired.
        """
        next_round = self.get_next_round(tournament.rounds)

        if next_round is None:
            return Result.invalid(reason="no more rounds to run.")

        if self.are_round_matches_defined(next_round):
            return Result.valid(value=next_round)

        round_players_result = self._set_round_players(
            tournament, players_by_standing, next_round
        )

        if not round_players_result:
            return round_players_result

        return Result.valid(value=next_round)

    def are_round_matches_defined(self, round: Round) -> bool:
        """Tells if the round has been paired.

        Args:
            round (Round): The round to read.

        Returns:
            bool: True when the round holds at least one match.
        """
        return bool(flat_round_matches([round]))

    def get_incomplete_round_matches(self, round: Round) -> list[RoundMatch]:
        """Gets the matches of the round that hold no score yet.

        A match is incomplete when neither of its players holds a score.

        Args:
            round (Round): The round to read.

        Returns:
            list[RoundMatch]: The matches left to play.
        """
        round_matches = flat_round_matches([round])
        incomplete_round_match: list[RoundMatch] = [
            round_match
            for round_match in round_matches
            if round_match.player_score_a.is_score_not_set
            and round_match.player_score_b.is_score_not_set
        ]
        return incomplete_round_match

    def incomplete_round_matches_found(self, incomplete_round_match: list[RoundMatch]):
        """Tells if the round holds a match left to play.

        Args:
            incomplete_round_match (list[RoundMatch]): The matches left to play.

        Returns:
            bool: True when at least one match is left to play.
        """
        return bool(incomplete_round_match)
