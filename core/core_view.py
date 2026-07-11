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
    if menu_item.code in MenuCode:
        return MenuColorHelper.back(value)

    if menu_item.sub_menus:
        return MenuColorHelper.navigation(value)

    return MenuColorHelper.action(value)


class CoreView(Generic[TModel]):

    def __init__(self, console: Console) -> None:
        self.console = console

    def prompt(self, value: str):
        return self.console.input(ColorHelper.input(f"{value} : "))

    def prompt_action(self) -> str:
        return self.console.input(ColorHelper.input("Select choice : ")).upper()

    def render_invalid_input(self, reason: str) -> None:
        self.console.print(ColorHelper.invalid(reason))

    def render_success(self, success_message: str) -> None:
        self.console.print(ColorHelper.success(success_message))

    def skip_line(self) -> None:
        self.console.print()

    def prompt_menu_choice(self) -> str:
        return self.console.input(ColorHelper.input("Enter key menu : "))

    def render_menu_items(self, menu_items: list[MenuItem], title: str = ""):
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
