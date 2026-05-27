from __future__ import annotations
from typing import TYPE_CHECKING

from models.menu_item import MenuItem
from config.menu_definitions import EXIT_ITEM

if TYPE_CHECKING:
    from views.menu_display import MenuDisplay


class MenuRunner:
    actual_item: MenuItem

    def __init__(
        self,
        root_item: MenuItem,
        menu_display: MenuDisplay,
    ):
        self.actual_item = root_item
        self.menu_display = menu_display

    def run_menu(self) -> None:
        exit = False

        while not exit:
            child_items = self.actual_item.build_items()

            self.menu_display.display_items(child_items)

            user_choice = self.menu_display.display_choice_asking()
            selected_item = child_items.get(user_choice, None)

            if selected_item is None:
                self.menu_display.display_invalid_choice()
                continue

            if selected_item == EXIT_ITEM:
                exit = True
                continue

            if selected_item.child_items:
                self.actual_item = selected_item

            selected_item.run()
