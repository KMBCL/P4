from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console


from view.menu import MenuView


from controllers.handlers.menu import (
    MenuPromptHandler,
    MenuRendererHandler,
)
from menu.menu import MenuController

if TYPE_CHECKING:
    from menu.registry import ActionRouting


def build_menu_controller(console: Console, registry: ActionRouting) -> MenuController:
    view = MenuView(console)
    prompt_handler = MenuPromptHandler(view)
    renderer_handler = MenuRendererHandler(view)
    menu_controller = MenuController(prompt_handler, renderer_handler, registry)

    return menu_controller
