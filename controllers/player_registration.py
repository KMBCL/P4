from typing import Any

from rich.console import Console

from core.core_controller import CoreController

from view.player_registration import PlayerRegistrationView

from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.handlers.player_registration import (
    PlayerRegistrationPromptHandler,
    PlayerRegistrationRenderHandler,
)
from controllers.shortcuts.player_registration import PlayerRegistrationShortcut
from controllers.menu_state import MenuState

from repository.player_registration import PlayerRegistrationRepository


class PlayerRegistrationController(CoreController):

    def __init__(self, console: Console):
        view = PlayerRegistrationView(console=console)
        self.repository = PlayerRegistrationRepository()
        self.prompt_handler = PlayerRegistrationPromptHandler(view=view)
        self.render_controller = PlayerRegistrationRenderHandler(view=view)

        action_runner = ActionRunner(
            target_controller=self,
            action_routing=ACTION_ROUTING,
            prompt_handler=self.prompt_handler,
            render_controller=self.render_controller,
        )
        super().__init__(action_runner=action_runner)

    def register_player(self) -> None:
        self.repository.save_new_player_registration(
            user_input=self.prompt_handler.get_player_registration_input()
        )


ACTION_ROUTING: ActionRouting = {
    PlayerRegistrationShortcut.REGISTER_PLAYER.value.shortcut: PlayerRegistrationController.register_player,
    PlayerRegistrationShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
