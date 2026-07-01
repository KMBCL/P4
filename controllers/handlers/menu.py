from typing import Any

from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer

from core.core_view import CoreView
from controllers.validators.menu import MenuValidator
from models.menu import MenuItem


class MenuPromptHandler(CorePromptHandler[CoreView[Any]]):

    def prompt_menu_key(self, available_items: list[MenuItem]) -> str:
        return self.prompt(
            self.view.list_view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(
                user_input, available_items
            ),
        )


class MenuRendererHandler(CoreRenderer):

    def render_menu_items(self, menu_items: list[MenuItem]) -> None:
        self.view.list_view.render_menu_items(menu_items)
