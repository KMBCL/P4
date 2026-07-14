"""Builds the menu controller, from the handlers, the registry and the service."""

from service.build import (
    menu_service,
)
from controllers.handlers.build import (
    menu_prompt_handler,
    menu_renderer_handler,
)

from controllers.menu import MenuController

from controllers.registry import REGISTRY

menu_controller = MenuController(
    menu_prompt_handler,
    menu_renderer_handler,
    REGISTRY,
    menu_service,
)
