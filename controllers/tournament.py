from views.tournament import TournamentView


from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.shortcuts.tournament import TournamentShortcut

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from controllers.menu_state import MenuState

from models.tournament import Tournament, TournamentInputData
from repository.tournament import TournamentRepository


class TournamentController:

    def __init__(self, view: TournamentView) -> None:
        self.repository = TournamentRepository()
        self.prompt_handler = TournamentPromptHandler(view=view)
        self.render_controller = TournamentRenderHandler(view=view)

        self.action_runner = ActionRunner(
            target_controller=self,
            action_routing=ACTION_ROUTING,
            prompt_handler=self.prompt_handler,
            render_controller=self.render_controller,
        )

    def build_new(self, user_input: TournamentInputData, new_pk: int):
        new = Tournament.from_user_input(new_pk=new_pk, user_input=user_input)
        return new

    def get_tournament_input(self) -> TournamentInputData:
        return TournamentInputData(
            name=self.prompt_handler.prompt_name(),
            place=self.prompt_handler.prompt_place(),
            start_date=self.prompt_handler.prompt_start_date(),
            end_date=self.prompt_handler.prompt_end_date(),
            description=self.prompt_handler.prompt_description(),
            round_count=self.prompt_handler.prompt_round_count(),
        )

    def create_new_tournament(self):
        tournament = self.build_new(
            user_input=self.get_tournament_input(), new_pk=self.repository.make_new_pk()
        )
        self.repository.write_data(json_data=tournament.to_json())

    def show_tournaments(self):
        tournaments = self.repository.get_models()
        self.render_controller.render_tournaments(tournaments)

    def show_filtered_tournaments(self):
        pass

    def run(self):
        self.action_runner.run()


ACTION_ROUTING: ActionRouting = {
    TournamentShortcut.CREATE_TOURNAMENT.value.shortcut: TournamentController.create_new_tournament,
    TournamentShortcut.TOURNAMENTS.value.shortcut: TournamentController.show_tournaments,
    TournamentShortcut.FILTER_TOURNAMENTS.value.shortcut: TournamentController.show_filtered_tournaments,
    TournamentShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
