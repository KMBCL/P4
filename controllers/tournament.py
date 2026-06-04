from rich.console import Console


from core.core_controller import CoreController

from view.tournament import TournamentView


from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.shortcuts.tournament import TournamentShortcut

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from controllers.menu_state import MenuState


from repository.tournament import TournamentRepository


class TournamentController(CoreController):

    def __init__(self, console: Console) -> None:

        view: TournamentView = TournamentView(console=console)
        self.repository = TournamentRepository()
        self.prompt_handler = TournamentPromptHandler(view=view)
        self.render_controller = TournamentRenderHandler(view=view)

        action_runner = ActionRunner(
            target_controller=self,
            action_routing=ACTION_ROUTING,
            prompt_handler=self.prompt_handler,
            render_controller=self.render_controller,
        )

        super().__init__(action_runner=action_runner)

    def create_new_tournament(self):
        self.repository.save_new_tournament(
            user_input=self.prompt_handler.get_tournament_input()
        )

    def show_tournaments(self):
        tournaments = self.repository.get_models()
        self.render_controller.render_tournaments(tournaments)

    def show_filtered_tournaments(self):
        pass


ACTION_ROUTING: ActionRouting = {
    TournamentShortcut.CREATE_TOURNAMENT.value.shortcut: TournamentController.create_new_tournament,
    TournamentShortcut.TOURNAMENTS.value.shortcut: TournamentController.show_tournaments,
    TournamentShortcut.FILTER_TOURNAMENTS.value.shortcut: TournamentController.show_filtered_tournaments,
    TournamentShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
