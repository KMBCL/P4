from typing import Any

from core.core_view import CoreView
from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer
from core.core_controller import CoreController

from controllers.player import PlayerController
from controllers.tournament import TournamentController

from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.shortcuts.main import MainShortcut

from controllers.menu_state import MenuState

from rich.console import Console


from views.player import PlayerView
from views.tournament import TournamentView

from controllers.player import PlayerController
from controllers.tournament import TournamentController
from controllers.handlers.action_prompt import ActionPromptHandler


class MainController(CoreController):

    def __init__(self, console: Console) -> None:

        self.player_controller = PlayerController(
            PlayerView(console=console),
        )
        self.tournament_controller = TournamentController(
            TournamentView(console=console),
        )

        main_view = CoreView[Any](console)
        self.prompt_handler = CorePromptHandler(
            action_prompt_handler=ActionPromptHandler[Any](view=main_view),
            action_shortcuts=MainShortcut,
        )

        action_runner = ActionRunner(
            target_controller=self,
            action_routing=ACTION_ROUTING,
            prompt_handler=self.prompt_handler,
            render_controller=CoreRenderer(view=main_view),
        )

        super().__init__(action_runner=action_runner)

    def run_player_controller(self) -> None:
        self.player_controller.run()

    def run_tournament_controller(self) -> None:
        self.tournament_controller.run()


ACTION_ROUTING: ActionRouting = {
    MainShortcut.HANDLE_PLAYERS.value.shortcut: MainController.run_player_controller,
    MainShortcut.HANDLE_TOURNAMENTS.value.shortcut: MainController.run_tournament_controller,
    MainShortcut.EXIT.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
