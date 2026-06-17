from __future__ import annotations

from typing import Any

from core.core_view import CoreView
from models.menu import MenuItem


class MenuView(CoreView[Any]):

    def prompt_menu_choice(self) -> str:
        return self.console.input("Select key menu : ")

    def show_menu_items(self, menu_items: list[MenuItem]):
        MENU_START = 1
        menu_key = MENU_START
        for menu_item in menu_items:
            displayed = f"{menu_key} - {menu_item.title}"
            self.console.print(displayed)
            menu_key += 1
