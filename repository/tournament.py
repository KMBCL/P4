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

    def make_player_pairs(
        self,
        tournament: Tournament,
    ) -> list[tuple[str, str]]:
        pairs: list[tuple[str, str]] = []
        chess_ids = tournament.registered_player_chess_ids
        if self.is_first_round(tournament.rounds):
            random.shuffle(chess_ids)

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

    def set_round_players(self, tournament: Tournament, round_name: str) -> Result:
        player_pairs_check_result = self.check_registered_players_pairs(tournament)
        if not player_pairs_check_result:
            return player_pairs_check_result

        shuffled_pairs: list[tuple[str, str]] = self.make_player_pairs(tournament)
        round = tournament.get_round(round_name)
        if round is None:
            return Result.invalid(
                reason=f"Round : {round_name} not found in tournament"
            )
        round.set_round_players(player_pairs=shuffled_pairs)

        return Result.valid(value=tournament)


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

    def write_tournament(self, tournament: dict[str, Any]) -> None:
        raw_tournaments = self.read_json_file()
        tournaments_by_pk = self.to_data_dict(raw_data=raw_tournaments, field_name="pk")
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

        self.write_tournament(result.required_value)
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

    def set_round_matches(self, tournament_pk: str, round_name: str) -> Result:
        tournament_result = self.get_tournament_by_pk(
            tournament_pk=tournament_pk,
        )
        if not tournament_result:
            return tournament_result

        tournament: Tournament = Tournament.from_json(tournament_result.required_value)
        round_handler = RoundHandler()
        tournament_result = round_handler.set_round_players(
            tournament=tournament, round_name=round_name
        )
        tournament_json = tournament.to_json()
        self.write_tournament(tournament_json)
        return Result.valid()
