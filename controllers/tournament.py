from __future__ import annotations

from typing import Callable

from views.tournament import TournamentView

from controllers.validators.action import ActionValidator

from controllers.shortcuts.tournament import TournamentShortcuts

from controllers.handlers.date_prompt import DatePromptHandler
from controllers.handlers.action_prompt import ActionPromptHandler

from models.tournament import Tournament, TournamentInputData
from repository.tournament import TournamentRepository


class TournamentPromptHandler:

    def __init__(self, view: TournamentView) -> None:
        self.view = view
        self.date_prompt_handler = DatePromptHandler[Tournament](self.view)
        self.action_prompt_handler = ActionPromptHandler[Tournament](self.view)

    def prompt_action(self) -> str:
        return self.action_prompt_handler.prompt_action(
            action_shortcuts=TournamentShortcuts
        )

    def prompt_name(self) -> str:
        return self.view.prompt_name()

    def prompt_place(self) -> str:
        return self.view.prompt_place()

    def prompt_description(self) -> str:
        return self.view.prompt_description()

    def prompt_round_count(self) -> str:
        return self.view.prompt_round_count()

    def prompt_start_date(self) -> str:
        return self.date_prompt_handler.prompt_date(self.view.prompt_start_date)

    def prompt_end_date(self) -> str:
        return self.date_prompt_handler.prompt_date(self.view.prompt_end_date)


class TournamentRenderHandler:

    def __init__(self, view: TournamentView) -> None:
        self.view = view

    def render_tournaments(self, tournaments: list[Tournament]):
        self.view.render_models(tournaments)


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

    def create_new_tournament(self) -> str:
        tournament = self.build_new(
            user_input=self.get_tournament_input(), new_pk=self.repository.make_new_pk()
        )
        self.repository.write_data(json_data=tournament.to_json())
        return "success!"

    def show_tournaments(self):
        tournaments = self.repository.get_models()
        self.render_controller.render_tournaments(tournaments)

    def run(self) -> None:
        running = True
        while running:
            action = self.prompt_controller.prompt_action()
            if action == TournamentShortcuts.CREATE_TOURNAMENT:
                self.create_new_tournament()
                continue

            if action == TournamentShortcuts.TOURNAMENTS:
                self.show_tournaments()
                continue
