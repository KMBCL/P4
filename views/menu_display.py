from __future__ import annotations
from typing import TYPE_CHECKING

from config.menu_constants import EXIT_SHORCUT, BACK_SHORTCUT

from rich.console import Console

if TYPE_CHECKING:
    from models.menu_item import MenuItem


class ColorPicker:
    exit_color = "bold red"
    back_color = "bold yellow"
    navigation_color = "bold cyan"
    action_color = "bold green"

    @classmethod
    def pickup_color(cls, key: str, item: MenuItem) -> str:
        if key == EXIT_SHORCUT:
            return cls.exit_color

        if key == BACK_SHORTCUT:
            return cls.back_color

        if not item.child_items:
            return cls.action_color

        return cls.navigation_color


class MenuDisplay:

    def __init__(self) -> None:
        self.console = Console()

    def format_item_display(self, key: str, item: MenuItem) -> str:
        shortcut_color = ColorPicker.pickup_color(key=key, item=item)
        return f"[{shortcut_color}]{key}[/{shortcut_color}] - {item.title}"

    def display_items(self, items: dict[str, MenuItem]) -> None:
        for key, item in items.items():
            self.console.print(
                self.format_item_display(
                    key=key,
                    item=item,
                )
            )

    def display_invalid_choice(self) -> None:
        self.console.print("Please select available choices")

    def display_choice_asking(self) -> str:
        return self.console.input("Sélectionner une action : ").upper()
