from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.console import Console


from core.core_view import CoreView, ListView


from controllers.handlers.menu import (
    MenuPromptHandler,
    MenuRendererHandler,
)
from controllers.menu import MenuController

if TYPE_CHECKING:
    from menu.registry import ActionRouting


def build_menu_controller(
    console: Console,
    list_view: ListView,
    registry: ActionRouting,
) -> MenuController:
    view = CoreView[Any](console)
    prompt_handler = MenuPromptHandler(view)
    renderer_handler = MenuRendererHandler(view)
    menu_controller = MenuController(prompt_handler, renderer_handler, registry)

    return menu_controller
