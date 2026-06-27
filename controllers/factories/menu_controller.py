from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.console import Console


from core.core_view import CoreView, ListView
from models.menu import MenuStructure

from controllers.handlers.menu import (
    MenuPromptHandler,
    MenuRendererHandler,
)
from controllers.menu import MenuController

if TYPE_CHECKING:
    from registry import ActionRouting


def build_menu_controller(
    console: Console,
    list_view: ListView,
    registry: ActionRouting,
    menu_structure: MenuStructure,
) -> MenuController:
    view = CoreView[Any](console)
    prompt_handler = MenuPromptHandler(view)
    renderer_handler = MenuRendererHandler(view)
    menu_controller = MenuController(
        prompt_handler,
        renderer_handler,
        registry,
        menu_structure,
    )

    return menu_controller
