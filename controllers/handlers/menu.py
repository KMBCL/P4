"""Prompts and renders the menu."""

from typing import Any

from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer

from core.core_view import CoreView
from controllers.validators.menu import MenuValidator
from models.menu import MenuItem


class MenuPromptHandler(CorePromptHandler[CoreView[Any]]):
    """Asks the user to pick a menu entry, until the choice designates one."""

    def prompt_menu_key(self, available_items: list[MenuItem]) -> str:
        """Asks the user to pick one of the displayed entries.

        Args:
            available_items (list[MenuItem]): The entries currently displayed.

        Returns:
            str: The raw choice, once validated.
        """
        return self.prompt(
            self.view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(
                user_input, available_items
            ),
        )


class MenuRendererHandler(CoreRenderer):
    """Prints the menu entries."""

    def render_menu_items(self, menu_items: list[MenuItem]) -> None:
        """Prints the entries the user picks from.

        Args:
            menu_items (list[MenuItem]): The entries to print.
        """
        self.view.render_menu_items(menu_items)
