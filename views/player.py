from __future__ import annotations

from dataclasses import dataclass, fields, Field
from typing import TYPE_CHECKING, Any


from controllers.player_shortcuts import PlayerShortcuts

if TYPE_CHECKING:
    from models.player import Player
    from rich.console import Console


class PlayerView:

    def __init__(self, console: Console) -> None:
        self.console: Console = console

    def prompt_chess_id(self) -> str:
        return self.console.input("Chess id - Ex: 'AB13579' : ")

    def prompt_last_name(self) -> str:
        return self.console.input("Last name : ")

    def prompt_first_name(self) -> str:
        return self.console.input("First name : ")

    def prompt_birthdate(self) -> str:
        return self.console.input("Birthdate - 'YYYY-MM-DD' : ")

    def render_invalid_input(self, reason: str) -> None:
        self.console.print(reason)

    def render_available_actions(self):
        self.console.print("Select : ")
        self.console.print(f"{PlayerShortcuts.PLAYERS} - Show all players")
        self.console.print(f"{PlayerShortcuts.CREATE_PLAYER} - Create player")

    def prompt_action(self) -> str:
        user_input = self.console.input("Select choice : ").upper()
        return user_input

    def format_field(self, player: Player, field: Field[Any]) -> str:
        return f"{field.name}={getattr(player,field.name)}"

    def format_player(self, player: Player) -> str:
        formattedf_fields = [
            self.format_field(player, field) for field in fields(player)
        ]
        return " - ".join(formattedf_fields)

    def render_players(self, players: list[Player]):
        for player in players:
            formatted_player = self.format_player(player)
            self.console.print(formatted_player)
        self.console.print(f"total : {len(players)}")
