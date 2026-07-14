"""Applies the rules governing the players."""

from typing import TypeAlias

from core.result import Result


from repository.repository import Repository
from repository.paths import PLAYER_DIR
from repository.player import PlayerJSON

from models.player import Player, PlayerInputData
from models.tournament import Tournament

from service.helpers.sort import sort_players_by_last_name

Players: TypeAlias = list[Player]


class PlayerService:
    """Creates and reads the players, whose chess id must stay unique."""

    def __init__(self, repository: Repository) -> None:
        """Holds the repository the players are stored in.

        Args:
            repository (Repository): The repository to read and write through.
        """
        self.repository = repository

    def get_unregistered_players(
        self, players: Players, tournament: Tournament
    ) -> Result:
        """Gets the players not registered to the tournament yet.

        Args:
            players (Players): The players to filter.
            tournament (Tournament): The tournament to register to.

        Returns:
            Result:
                - A valid result carrying the players left to register.
                - An invalid one when every given player is already registered.
        """
        unregistered_players: Players = [
            player for player in players if player not in tournament.registered_players
        ]
        if not unregistered_players:
            return Result.invalid("All players matching are already registered")

        return Result.valid(value=unregistered_players)

    def _get_players(self) -> Players:
        """Reads every stored player.

        Returns:
            Players: The players.
        """
        return [
            PlayerJSON.from_json(raw_player)
            for raw_player in self.repository.get_raw_models(PLAYER_DIR)
        ]

    @staticmethod
    def _extract_similar_players(player_name: str, players: Players) -> Players:
        """Extracts the players whose last name contains the given one.

        The comparison ignores case, and matches a part of the last name.

        Args:
            player_name (str): The last name, whole or partial, to look for.
            players (Players): The players to filter.

        Returns:
            Players: The matching players.
        """
        return [
            player
            for player in players
            if player_name.lower() in player.last_name.lower()
        ]

    def get_player_by_name(self, player_name: str) -> Result:
        """Reads the players whose last name contains the given one.

        Args:
            player_name (str): The last name, whole or partial, to look for.

        Returns:
            Result:
                - A valid result carrying the matching players.
                - An invalid one when no last name matches.
        """
        players = self._get_players()
        similar_players = PlayerService._extract_similar_players(player_name, players)
        if not similar_players:
            return Result.invalid(
                reason=f"No players found with {player_name} last_name"
            )

        return Result.valid(value=similar_players)

    def get_player_by_chess_id(self, chess_id: str) -> Result:
        """Reads the single player holding the given chess id.

        Args:
            chess_id (str): The chess id to look for.

        Returns:
            Result:
                - A valid result carrying the player.
                - An invalid one when no player holds that chess id.
        """
        chess_id_filter: dict[str, str] = {"chess_id": chess_id}
        players = self.repository.get_filtered_raw_models(PLAYER_DIR, chess_id_filter)
        if not players:
            return Result.invalid(f"No player found with pk : {chess_id}")

        player = PlayerJSON.from_json(players[0])
        return Result.valid(player)

    def can_save(self, chess_id: str) -> Result:
        """Tells whether a chess id is free to be taken by a new player.

        The valid result carries no value: it is read with is_valid only. Gate mode.

        Args:
            chess_id (str): The chess id awaited by the new player.

        Returns:
            Result:
                - A valid result, holding no value, when the chess id is free.
                - An invalid one when a player already holds that chess id.
        """
        chess_id_filter: dict[str, str] = {"chess_id": chess_id}
        players = self.repository.get_filtered_raw_models(PLAYER_DIR, chess_id_filter)
        if players:
            return Result.invalid(
                reason=f"Found existing players {players} with same chess_id {chess_id}"
            )

        return Result.valid()

    def _make_pk(self) -> str:
        """Builds the primary key following the ones already stored.

        Returns:
            str: The primary key of the next player.
        """
        players = self.repository.get_raw_models(PLAYER_DIR)
        return str(len(players) + 1)

    def create_new_player(self, player_input: PlayerInputData) -> Result:
        """Creates a player, and stores it.

        Args:
            player_input (PlayerInputData): The raw fields typed by the user.

        Returns:
            Result:
                - A valid result carrying the stored player.
                - An invalid one when its chess id is already taken.
        """
        can_save_result = self.can_save(player_input.chess_id)
        if not can_save_result.is_valid():
            return can_save_result

        player = Player.from_user_input(self._make_pk(), player_input)
        self.repository.save_new_raw_model(PLAYER_DIR, PlayerJSON.to_json(player))
        return Result.valid(
            value=player, success_message="Successfully saved new player!"
        )

    def get_players(self) -> Result:
        """Reads every stored player, ordered by last name.

        Returns:
            Result:
                - A valid result carrying the ordered players.
                - An invalid one when no player is stored.
        """
        players = self._get_players()
        if not players:
            return Result.invalid("No players found")

        sorted_players = sort_players_by_last_name(players)
        return Result.valid(sorted_players)
