from typing import Any

from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer

from core.core_view import CoreView
from view.menu import MenuView
from controllers.validators.menu import MenuValidator
from models.menu import MenuItem


class MenuPromptHandler(CorePromptHandler[MenuView]):

    def prompt_menu_key(self, available_items: list[MenuItem]) -> str:
        return self.prompt(
            self.view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(
                user_input, available_items
            ),
        )


class MenuRendererHandler(CoreRenderer):

    def __init__(self, view: MenuView) -> None:
        self.view = view

    def render_choice_menu(self, menu_items: list[MenuItem]) -> None:
        self.view.show_menu_items(menu_items)
