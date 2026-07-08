from __future__ import annotations


from typing import TYPE_CHECKING, Any, Generic, TypeVar

from core.color import ColorHelper, MenuColorHelper
from core.core_model import Model
from models.menu import MenuItem

if TYPE_CHECKING:
    from rich.console import Console


TModel = TypeVar("TModel", bound=Model[Any])


class CoreView(Generic[TModel]):

    def __init__(self, console: Console) -> None:
        self.console = console

    def prompt(self, value: str):
        return self.console.input(ColorHelper.title(f"{value} : "))

    def prompt_action(self) -> str:
        return self.console.input("Select choice : ").upper()

    def render_invalid_input(self, reason: str) -> None:
        self.console.print(f"[red]{reason}[/red]")

    def render_success(self, success_message: str) -> None:
        self.console.print(f"[green]{success_message}[/green]")

    def skip_line(self) -> None:
        self.console.print()

    def prompt_menu_choice(self) -> str:
        return self.console.input(ColorHelper.title("Enter key menu : "))

    def render_menu_items(self, menu_items: list[MenuItem]):
        self.skip_line()
        MENU_START = 1
        menu_key = MENU_START
        for menu_item in menu_items:
            displayed_menu = f"{menu_key} - {menu_item.title}"
            if menu_item.sub_menus:
                displayed = MenuColorHelper.navigation(displayed_menu)
            else:
                displayed = MenuColorHelper.action(displayed_menu)
            self.console.print(displayed)
            menu_key += 1

        self.skip_line()
