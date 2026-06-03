from views.tournament import TournamentView

from core.core_shortcuts import CoreShortcut
from controllers.shortcuts.tournament import TournamentShortcut

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from models.tournament import Tournament, TournamentInputData
from repository.tournament import TournamentRepository


class TournamentController:

    def __init__(self, view: TournamentView) -> None:
        self.repository = TournamentRepository()
        self.prompt_controller = TournamentPromptHandler(view=view)
        self.render_controller = TournamentRenderHandler(view=view)

    def build_new(self, user_input: TournamentInputData, new_pk: int):
        new = Tournament.from_user_input(new_pk=new_pk, user_input=user_input)
        return new

    def get_tournament_input(self) -> TournamentInputData:
        return TournamentInputData(
            name=self.prompt_controller.prompt_name(),
            place=self.prompt_controller.prompt_place(),
            start_date=self.prompt_controller.prompt_start_date(),
            end_date=self.prompt_controller.prompt_end_date(),
            description=self.prompt_controller.prompt_description(),
            round_count=self.prompt_controller.prompt_round_count(),
        )

    def create_new_tournament(self):
        tournament = self.build_new(
            user_input=self.get_tournament_input(), new_pk=self.repository.make_new_pk()
        )
        self.repository.write_data(json_data=tournament.to_json())

    def show_tournaments(self):
        tournaments = self.repository.get_models()
        self.render_controller.render_tournaments(tournaments)

    def run(self) -> None:
        running = True
        while running:
            action = self.prompt_controller.prompt_action()
            if action == TournamentShortcut.CREATE_TOURNAMENT.value.shortcut:
                self.create_new_tournament()
                continue

            if action == TournamentShortcut.TOURNAMENTS.value.shortcut:
                self.show_tournaments()
                continue

            if action == CoreShortcut.BACK.value.shortcut:
                continue
