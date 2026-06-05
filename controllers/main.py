from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer
from core.core_data_repository import CoreDataRepository
from core.core_controller import CoreController

from controllers.shortcuts.main import MainShortcut


class MainController(
    CoreController[
        CoreDataRepository,
        CorePromptHandler,
        CoreRenderer,
    ]
):

    def __init__(
        self,
        repository: CoreDataRepository,
        prompt_handler: CorePromptHandler,
        renderer_handler: CoreRenderer,
    ) -> None:
        super().__init__(repository, prompt_handler, renderer_handler)

    def run_handle_players(self) -> None:
        self.run_runner(runner_key=MainShortcut.HANDLE_PLAYERS.value.shortcut)

    def run_handle_tournaments(self) -> None:
        self.run_runner(runner_key=MainShortcut.HANDLE_TOURNAMENTS.value.shortcut)
