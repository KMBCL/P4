from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler

from view.tournament import TournamentView
from controllers.validators.date import DateValidator

from models.tournament import Tournament, TournamentInputData
from models.score import TournamentPlayerScore


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

    def render_standings(self, standings: list[TournamentPlayerScore]) -> None:
        self.view.console.print("*** Tournament standings ***")

        for standing in standings:
            self.view.console.print(
                f"{standing.tournement_score_value} - {standing.player.last_name} {standing.player.first_name}"
            )

    def render_tournament_details(self, tournament: Tournament) -> None:
        self.view.console.print("*** Tournament details ***")

        self.view.console.print(f"Tournament Name : {tournament.name}")
        self.view.console.print(f"Tournament start date : {tournament.start_date}")
        self.view.console.print(f"Tournament end date : {tournament.end_date}")
        self.view.console.print(f"Tournament player count : {tournament.player_count}")
        self.view.console.print(f"Tournament round count : {tournament.round_count}")
