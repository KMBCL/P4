from typing import Any

from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer

from core.core_view import CoreView
from view.menu import MenuView
from controllers.validators.menu import MenuValidator
from models.menu import MenuItem


class MenuPromptHandler(CorePromptHandler):

    def __init__(self, view: MenuView) -> None:
        self.view = view
        self.menu_validator = MenuValidator()

    def prompt_menu_key(self, available_items: list[MenuItem]) -> int:
        while True:
            user_input = self.view.prompt_menu_choice()

            user_input_result = self.menu_validator.validate_menu_choice(
                user_input, available_items
            )
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.required_reason)
                continue

            return int(user_input)


class MenuRendererHandler(CoreRenderer):

    def __init__(self, view: MenuView) -> None:
        self.view = view

    def render_choice_menu(self, menu_items: list[MenuItem]) -> None:
        self.view.show_menu_items(menu_items)
