from __future__ import annotations

from dataclasses import dataclass, fields, Field
from typing import TYPE_CHECKING, Any


from controllers.player_shortcuts import PlayerShortcuts

if TYPE_CHECKING:
    from models.tournament import Tournament
    from rich.console import Console


class TournamentView:

    def __init__(self, console: Console) -> None:
        self.console: Console = console

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

    def format_field(self, tournament: Tournament, field: Field[Any]) -> str:
        return f"{field.name}={getattr(tournament,field.name)}"

    def format_tournament(self, tournament: Tournament):
        formattedf_fields = [
            self.format_field(tournament, field) for field in fields(tournament)
        ]
        return " - ".join(formattedf_fields)

    def render_tournaments(self, tournaments: list[Tournament]):
        for tournament in tournaments:
            formatted_tournament = self.format_tournament(tournament)
            self.console.print(formatted_tournament)
        self.console.print(f"total : {len(tournaments)}")
