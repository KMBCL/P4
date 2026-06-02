from __future__ import annotations

from dataclasses import dataclass, fields, Field
from typing import TYPE_CHECKING, Any


from models.player import Player, PlayerInputData
from controllers.create_player import PlayerController, PlayerShortcuts

if TYPE_CHECKING:
    from rich.console import Console


class PlayerDisplay:

    def __init__(self, console: Console) -> None:
        self.console: Console = console
        self.controller: PlayerController = PlayerController()

    def prompt_chess_id(self):
        chess_id = self.console.input("Chess id - Ex: AB13579 : ")
        result = self.controller.validate_chess_id(user_input=chess_id)

        if not result:
            self.console.print(result.reason)
            self.prompt_chess_id()

        return chess_id

    def get_new_player_input(self) -> PlayerInputData:
        chess_id = self.prompt_chess_id()
        last_name = self.console.input("Last name : ")
        first_name = self.console.input("First name : ")

        player_prompt_data = PlayerInputData(
            chess_id=chess_id,
            last_name=last_name,
            first_name=first_name,
        )
        return player_prompt_data

    def prompt_new_player(self):
        new_player_input = self.get_new_player_input()
        result = self.controller.create_new_player(new_player_input)
        self.console.print(result)
        self.prompt_action()

    def handle_invalid_input(self, user_input: str) -> None:
        self.console.print(
            f"{user_input} is not valid! Please select available shortcut"
        )
        self.prompt_action()

    def render_available_actions(self):
        self.console.print("Select : ")
        self.console.print(f"{PlayerShortcuts.PLAYERS} - Show all players")
        self.console.print(f"{PlayerShortcuts.CREATE_PLAYER} - Create player")

    def prompt_action(self) -> None:
        self.render_available_actions()

        user_input = self.console.input("Select choice : ").upper()

        if user_input == PlayerShortcuts.PLAYERS:
            self.render_players()
            return None

        if user_input == PlayerShortcuts.CREATE_PLAYER:
            self.prompt_new_player()
            return None

        self.handle_invalid_input(user_input)

    def format_field(self, player: Player, field: Field[Any]) -> str:
        return f"{field.name}={getattr(player,field.name)}"

    def format_player(self, player: Player) -> str:
        formattedf_fields = [
            self.format_field(player, field) for field in fields(player)
        ]
        return " - ".join(formattedf_fields)

    def render_players(self):
        players = self.controller.get_players()
        for player in players:
            formatted_player = self.format_player(player)
            self.console.print(formatted_player)
        self.console.print(f"total : {len(players)}")
        self.prompt_action()
