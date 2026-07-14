"""Provides the base every view is built on, and the colour of a menu entry."""

from __future__ import annotations


from typing import TYPE_CHECKING, Any, Generic, TypeVar

from core.color import ColorHelper, MenuColorHelper
from core.core_model import Model
from models.menu import MenuItem

from menu.constants import MenuCode

if TYPE_CHECKING:
    from rich.console import Console


TModel = TypeVar("TModel", bound=Model[Any])


def resolve_color(menu_item: MenuItem, value: str) -> str:
    """Colours a menu entry after what selecting it does.

    Args:
        menu_item (MenuItem): The entry to colour.
        value (str): The line displaying the entry.

    Returns:
        str: The coloured line.
    """
    if menu_item.code in MenuCode:
        return MenuColorHelper.back(value)

    if menu_item.sub_menus:
        return MenuColorHelper.navigation(value)

    return MenuColorHelper.action(value)


class CoreView(Generic[TModel]):
    """Bases a view, reading from and printing to a shared console."""

    def __init__(self, console: Console) -> None:
        """Holds the console the view reads from and prints to.

        Args:
            console (Console): The console shared by every view.
        """
        self.console = console

    def prompt(self, value: str):
        """Asks the user for a value.

        Args:
            value (str): The label naming the awaited value.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.console.input(ColorHelper.input(f"{value} : "))

    def prompt_action(self) -> str:
        """Asks the user for an action.

        Returns:
            str: The raw input, upper cased.
        """
        return self.console.input(ColorHelper.input("Select choice : ")).upper()

    def render_invalid_input(self, reason: str) -> None:
        """Prints the reason an input was rejected.

        Args:
            reason (str): The reason to print.
        """
        self.console.print(ColorHelper.invalid(reason))

    def render_success(self, success_message: str) -> None:
        """Prints the outcome of a successful action.

        Args:
            success_message (str): The message to print.
        """
        self.console.print(ColorHelper.success(success_message))

    def skip_line(self) -> None:
        """Prints an empty line."""
        self.console.print()

    def prompt_menu_choice(self) -> str:
        """Asks the user to choose a menu entry.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.console.input(ColorHelper.input("Enter key menu : "))

    def render_menu_items(self, menu_items: list[MenuItem], title: str = ""):
        """Prints the menu entries, numbered from one and coloured after their kind.

        Args:
            menu_items (list[MenuItem]): The entries to print.
            title (str): The title heading the entries. Defaults to none.
        """
        self.skip_line()
        self.console.print(ColorHelper.title(title))
        MENU_START = 1
        menu_key = MENU_START
        for menu_item in menu_items:
            displayed_menu = f"{menu_key} - {menu_item.title}"
            displayed = resolve_color(menu_item, displayed_menu)
            self.console.print(displayed)
            menu_key += 1

        self.skip_line()
