"""Applies the rules governing the registration of a player to a tournament."""

from __future__ import annotations

from typing import Any, TypeAlias

from core.result import Result

from models.tournament import Tournament
from models.player import Player

from service.player import PlayerService

Tournaments: TypeAlias = list[Tournament]


class PlayerRegistration:
    """Registers a player to a tournament, at most once."""

    def __init__(self, player_service: PlayerService) -> None:
        """Holds the service the players are read through.

        Args:
            player_service (PlayerService): The service to read the players.
        """
        self.player_service = player_service

    def check_if_player_already_registered(
        self,
        tournament: Tournament,
        player: Player,
    ) -> Result:
        """Tells if the player is free to be registered.

        The valid result carries no value: it is read with is_valid only. Gate mode.

        Args:
            tournament (Tournament): The tournament to register to.
            player (Player): The player to register.

        Returns:
            Result:
                - A valid result, holding no value, when the player is not
                  registered yet.
                - An invalid one when the player is already registered.
        """
        if player in tournament.registered_players:
            return Result.invalid(
                reason=f"Player with chess_id : {player.last_name} is already registered"
            )

        return Result.valid()

    def check_players_left(self, tournament: Tournament) -> Result:
        """Reads the players that could still be registered to the tournament.

        Args:
            tournament (Tournament): The tournament to register to.

        Returns:
            Result:
                - A valid result carrying every stored player.
                - An invalid one when no player is stored, or when every stored
                  player is already registered.
        """
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
        """Registers the player to the tournament.

        Args:
            tournament (Tournament): The tournament to register to.
            player (Player): The player to register.

        Returns:
            Result:
                - A valid result carrying the tournament, player registered.
                - An invalid one when the player is already registered.
        """
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
        """Extracts the stored records of the registered players.

        Args:
            raw_players (list[dict[str, Any]]): The stored records to filter.
            registered_chess_ids (list[str]): The chess ids of the registered
                players.

        Returns:
            list[dict[str, Any]]: The records of the registered players.
        """
        raw_registered_players = [
            raw_player
            for raw_player in raw_players
            if raw_player["chess_id"] in registered_chess_ids
        ]
        return raw_registered_players

    def to_players(self, registered_raw_players: list[str]) -> list[Player]:
        """Rebuilds the registered players from their chess ids.

        Args:
            registered_raw_players (list[str]): The chess ids of the registered
                players.

        Returns:
            list[Player]: The players found, which may be fewer than the chess
                ids given.
        """
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
        """Tells if a chess id is held by one of the given records.

        Args:
            chess_id (str): The chess id to look for.
            players (list[dict[str, Any]]): The stored records to search.

        Returns:
            bool: True when a record holds that chess id.
        """
        chess_ids: list[str] = [player["chess_id"] for player in players]
        return chess_id in chess_ids
