from __future__ import annotations


from typing import TYPE_CHECKING, Any

from rich.console import Console

from core.core_view import CoreView
from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer
from core.core_data_repository import CoreDataRepository
from core.core_model import Model


from controllers.main import MainController
from controllers.handlers.action import ActionPromptHandler


from controllers.shortcuts.main import MainShortcut
from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.menu_state import MenuState

ACTION_ROUTING: ActionRouting = {
    MainShortcut.HANDLE_PLAYERS.value.shortcut: MainController.run_handle_players,
    MainShortcut.HANDLE_TOURNAMENTS.value.shortcut: MainController.run_handle_tournaments,
    MainShortcut.EXIT.value.shortcut: lambda *args: MenuState.break_loop(),
}


def build_main_controller(console: Console) -> MainController:
    view = CoreView[Any](console=console)
    repository = CoreDataRepository[Any](model_class=Model)
    action_prompt_handler = ActionPromptHandler[Any](view=view)
    prompt_handler = CorePromptHandler(
        action_prompt_handler=action_prompt_handler,
        action_shortcuts=MainShortcut,
    )
    renderer_handler = CoreRenderer(view=view)
    main_controller = MainController(
        repository=repository,
        prompt_handler=prompt_handler,
        renderer_handler=renderer_handler,
    )

    return main_controller


def build_main_action_runner(console: Console) -> ActionRunner:
    main_controler = build_main_controller(console=console)
    action_runner = ActionRunner(
        target_controller=main_controler, action_routing=ACTION_ROUTING
    )

    return action_runner
