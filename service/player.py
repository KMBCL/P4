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

    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def get_unregistered_players(
        self, players: Players, tournament: Tournament
    ) -> Result:
        unregistered_players: Players = [
            player for player in players if player not in tournament.registered_players
        ]
        if not unregistered_players:
            return Result.invalid("All players matching are already register")

        return Result.valid(value=unregistered_players)

    def _get_players(self) -> Players:
        return [
            PlayerJSON.from_json(raw_player)
            for raw_player in self.repository.get_raw_models(PLAYER_DIR)
        ]

    @staticmethod
    def _extract_similar_players(player_name: str, players: Players) -> Players:
        return [
            player
            for player in players
            if player_name.lower() in player.last_name.lower()
        ]

    def get_player_by_name(self, player_name: str) -> Result:
        players = self._get_players()
        similar_players = PlayerService._extract_similar_players(player_name, players)
        if not similar_players:
            return Result.invalid(
                reason=f"No players found with {player_name} last_name"
            )

        return Result.valid(value=similar_players)

    def get_player_by_chess_id(self, chess_id: str) -> Result:
        chess_id_filter: dict[str, str] = {"chess_id": chess_id}
        players = self.repository.get_filtered_raw_models(PLAYER_DIR, chess_id_filter)
        if not players:
            return Result.invalid(f"No player found with pk : {chess_id}")

        player = PlayerJSON.from_json(players[0])
        return Result.valid(player)

    def can_save(self, chess_id: str) -> Result:
        chess_id_filter: dict[str, str] = {"chess_id": chess_id}
        players = self.repository.get_filtered_raw_models(PLAYER_DIR, chess_id_filter)
        if players:
            return Result.invalid(
                reason=f"Found existing players {players} with same chess_id {chess_id}"
            )

        return Result.valid()

    def _make_pk(self) -> str:
        players = self.repository.get_raw_models(PLAYER_DIR)
        return str(len(players) + 1)

    def create_new_player(self, player_input: PlayerInputData) -> Result:
        can_save_resut = self.can_save(player_input.chess_id)
        if not can_save_resut.is_valid():
            return can_save_resut

        player = Player.from_user_input(self._make_pk(), player_input)
        self.repository.save_new_raw_model(PLAYER_DIR, PlayerJSON.to_json(player))
        return Result.valid(
            value=player, success_message="Successfully saved new player!"
        )

    def get_players(self) -> Result:
        players = self._get_players()
        if not players:
            return Result.invalid("No players found")

        sorted_players = sort_players_by_last_name(players)
        return Result.valid(sorted_players)
