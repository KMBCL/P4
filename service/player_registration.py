from __future__ import annotations

from typing import Any, TypeAlias

from core.result import Result

from models.tournament import Tournament
from models.player import Player

from service.player import PlayerService

Tournaments: TypeAlias = list[Tournament]


class PlayerRegistration:

    def __init__(self, player_service: PlayerService) -> None:
        self.player_service = player_service

    def check_if_player_already_registered(
        self,
        tournament: Tournament,
        player: Player,
    ) -> Result:
        if player in tournament.registered_players:
            return Result.invalid(
                reason=f"Player with chess_id : {player.last_name} is already registered"
            )

        return Result.valid()

    def check_players_left(self, tournament: Tournament) -> Result:
        players_result = self.player_service.get_players()
        if not players_result:
            return Result.invalid("No existing players to register")

        players: list[Player] = players_result.get_value()
        if len(players) == len(tournament.registered_players):
            return Result.invalid("No players left to register")

        return Result.valid(players)

    def register_player_to_tournament(
        self,
        tournament: Tournament,
        player: Player,
    ) -> Result:

        already_registered_result = self.check_if_player_already_registered(
            tournament,
            player,
        )
        if not already_registered_result.is_valid():
            return already_registered_result

        tournament.registered_players.append(player)
        return Result.valid(value=tournament)

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

    def to_players(self, registered_raw_players: list[str]) -> list[Player]:
        players: list[Player] = []
        pk_errors: list[str] = []
        for raw_registered_player in registered_raw_players:
            result = self.player_service.get_player_by_chess_id(raw_registered_player)
            if not result:
                pk_errors.append(raw_registered_player)
                continue

            player: Player = result.get_value()
            players.append(player)
        return players

    def validate_chess_id_exists(
        self, chess_id: str, players: list[dict[str, Any]]
    ) -> bool:
        chess_ids: list[str] = [player["chess_id"] for player in players]
        return chess_id in chess_ids
