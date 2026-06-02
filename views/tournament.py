from __future__ import annotations

from dataclasses import dataclass, fields, Field
from typing import TYPE_CHECKING, Any

from views.core_view import CoreView

if TYPE_CHECKING:
    from models.tournament import Tournament


class TournamentView(CoreView[Tournament]):

    def prompt_name(self) -> str:
        return self.console.input("Name : ")

    def prompt_place(self) -> str:
        return self.console.input("Place : ")

    def prompt_start_date(self) -> str:
        return self.console.input("Start date - 'YYYY-MM-DD' : ")

    def prompt_end_date(self) -> str:
        return self.console.input("End date - 'YYYY-MM-DD' : ")

    def prompt_description(self) -> str:
        return self.console.input("Description : ")

    def prompt_round_count(self) -> str:
        return self.console.input("Round count - default=4 : ")

    def render_available_actions(self):
        self.console.print("Select : ")

    def prompt_action(self) -> str:
        return self.console.input("Select choice : ").upper()
