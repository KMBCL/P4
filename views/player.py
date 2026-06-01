from __future__ import annotations

from dataclasses import dataclass, fields, Field
from typing import TYPE_CHECKING, Any


from models.player import Player, PlayerInputData
from controllers.create_player import PlayerController, PlayerShortcuts, Result

if TYPE_CHECKING:
    from rich.console import Console


class PlayerDisplay:

    def __init__(self, console: Console) -> None:
        self.console = console
        self.controller = PlayerController()

    def input_chess_id(self):
        chess_id = self.console.input("Chess id - Ex: AB13579 : ")
        result = self.controller.validate_chess_id(user_input=chess_id)

        if not result:
            self.console.print(result.reason)
            self.input_chess_id()

        return chess_id

    def get_new_player_input(self) -> PlayerInputData:
        chess_id = self.input_chess_id()
        last_name = self.console.input("Last name : ")
        first_name = self.console.input("First name : ")

        player_input_data = PlayerInputData(
            chess_id=chess_id,
            last_name=last_name,
            first_name=first_name,
        )
        return player_input_data

    def input_new_player(self):
        new_player_input = self.get_new_player_input()
        result = self.controller.create_new_player(new_player_input)
        self.console.print(result)
        self.input_action()

    def handle_invalid_input(self, user_input: str) -> None:
        self.console.print(
            f"{user_input} is not valid! Please select available shortcut"
        )
        self.input_action()

    def input_action(self) -> None:
        self.console.print("Select : ")
        self.console.print(f"{PlayerShortcuts.PLAYERS} - Show all players")
        self.console.print(f"{PlayerShortcuts.CREATE_PLAYER} - Create player")

        user_input = input("Select choice : ").upper()

        if user_input == PlayerShortcuts.PLAYERS:
            self.output_players()
            return None

        if user_input == PlayerShortcuts.CREATE_PLAYER:
            self.input_new_player()
            return None

        self.handle_invalid_input(user_input)

    def format_attribute(self, player: Player, field: Field[Any]) -> str:
        return f"{field.name}={getattr(player,field.name)}"

    def add_attribute_separator(self, display: str) -> str:
        return display + " - " if display else display

    def format_player(self, player: Player) -> str:
        formatted_player: str = ""

        for field in fields(player):
            formatted_attribute = self.format_attribute(player, field)
            formatted_player = self.add_attribute_separator(formatted_player)
            formatted_player = formatted_player + formatted_attribute
        return formatted_player

    def output_players(self):
        players = self.controller.get_players()
        for player in players:
            formatted_player = self.format_player(player)
            self.console.print(formatted_player)
        self.console.print(f"total : {len(players)}")
        self.input_action()
