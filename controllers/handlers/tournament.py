from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler

from view.tournament import TournamentView
from controllers.validators.date import DateValidator

from models.tournament import Tournament, TournamentInputData


class TournamentPromptHandler(CorePromptHandler[TournamentView]):

    def get_tournament_input(self):
        return TournamentInputData(
            name=self.prompt_name(),
            place=self.prompt_place(),
            start_date=self.prompt_start_date(),
            end_date=self.prompt_end_date(),
            description=self.prompt_description(),
            round_count=self.prompt_round_count(),
        )

    def get_player_registration_input(self):
        return self.view.prompt_register_player()

    def prompt_name(self) -> str:
        return self.view.prompt_name()

    def prompt_place(self) -> str:
        return self.view.prompt_place()

    def prompt_description(self) -> str:
        return self.view.prompt_description()

    def prompt_round_count(self) -> str:
        return self.view.prompt_round_count()

    def prompt_start_date(self) -> str:
        return self.prompt(self.view.prompt_start_date, DateValidator.validate_date)

    def prompt_end_date(self) -> str:
        return self.prompt(self.view.prompt_end_date, DateValidator.validate_date)

    def prompt_tournament_pk(self) -> str:
        return self.view.prompt_tournament_pk()


class TournamentRenderHandler(CoreRenderer):

    def __init__(self, view: TournamentView) -> None:
        self.view = view

    def render_tournaments(self, tournaments: list[Tournament]) -> None:
        self.view.console.print("*** Tournament list ***")

        for tournament in tournaments:
            self.view.console.print(
                f"'{tournament.name}' - Starts : {tournament.start_date} - Ends : {tournament.end_date} - Place : '{tournament.place}'"
            )

    def render_selected_tournament_name(self, tournament: Tournament) -> None:
        self.view.console.print(f"Selected tournament : {tournament.name}")
