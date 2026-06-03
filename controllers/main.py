from typing import Any

from controllers.player import PlayerController
from controllers.tournament import TournamentController

from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.shortcuts.main import MainShortcut

from controllers.menu_state import MenuState

from rich.console import Console

from views.player import PlayerView
from views.tournament import TournamentView
from views.main import MainView
from controllers.player import PlayerController
from controllers.tournament import TournamentController
from controllers.handlers.action_prompt import ActionPromptHandler

from core.core_handler import PromptHandler


class MainPromptHandler(PromptHandler):

    def __init__(self, view: MainView) -> None:
        self.view = view
        self.action_prompt_handler = ActionPromptHandler[Any](self.view)

    def prompt_action(self) -> tuple[str, dict[str, str]]:
        return self.action_prompt_handler.prompt_action(action_shortcuts=MainShortcut)


class MainRenderer:

    def __init__(self) -> None:
        pass


class MainController:

    def __init__(self, console: Console) -> None:
        self.view = MainView(console=console)
        self.player_controller = PlayerController(PlayerView(console=console))
        self.tournament_controller = TournamentController(
            TournamentView(console=console)
        )

        self.prompt_handler = MainPromptHandler(self.view)

        self.action_runner = ActionRunner(
            target_controller=self,
            action_routing=ACTION_ROUTING,
            prompt_handler=self.prompt_handler,
            render_controller=MainRenderer(),
        )

    def run_player_controller(self) -> None:
        self.player_controller.run()

    def run_tournament_controller(self) -> None:
        self.tournament_controller.run()

    def run(self):
        self.action_runner.run()


ACTION_ROUTING: ActionRouting = {
    MainShortcut.HANDLE_PLAYERS.value.shortcut: MainController.run_player_controller,
    MainShortcut.HANDLE_TOURNAMENTS.value.shortcut: MainController.run_tournament_controller,
    MainShortcut.EXIT.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
