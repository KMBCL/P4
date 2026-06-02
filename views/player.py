from __future__ import annotations

from typing import TYPE_CHECKING

from views.core_view import CoreView
from models.player import Player

from controllers.shortcuts.player import PlayerShortcuts


class PlayerView(CoreView[Player]):

    def prompt_chess_id(self) -> str:
        return self.console.input("Chess id - Ex: 'AB13579' : ")

    def prompt_last_name(self) -> str:
        return self.console.input("Last name : ")

    def prompt_first_name(self) -> str:
        return self.console.input("First name : ")

    def prompt_birthdate(self) -> str:
        return self.console.input("Birthdate - 'YYYY-MM-DD' : ")

    def render_available_actions(self):
        self.console.print("Select : ")
        self.console.print(f"{PlayerShortcuts.PLAYERS} - Show all players")
        self.console.print(f"{PlayerShortcuts.CREATE_PLAYER} - Create player")
