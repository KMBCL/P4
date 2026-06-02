from __future__ import annotations

from views.core_view import CoreView
from models.tournament import Tournament

from controllers.shortcuts.tournament import TournamentShortcut


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

    def prompt_action(self) -> str:
        return self.console.input("Select choice : ").upper()
