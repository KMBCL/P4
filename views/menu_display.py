from __future__ import annotations
from typing import TYPE_CHECKING

from config.menu_constants import EXIT_SHORTCUT, BACK_SHORTCUT

from rich.console import Console

if TYPE_CHECKING:
    from models.menu_item import MenuItem


class ColorPicker:
    exit_color = "bold red"
    back_color = "bold yellow"
    navigation_color = "bold cyan"
    action_color = "bold green"
    invalid_color = "red"
    input_awaiting_color = "green"

    @classmethod
    def pickup_color(cls, key: str, item: MenuItem) -> str:
        if key == EXIT_SHORTCUT:
            return cls.exit_color

        if key == BACK_SHORTCUT:
            return cls.back_color

        if not item.child_items:
            return cls.action_color

        return cls.navigation_color


class MenuDisplay:

    def __init__(self) -> None:
        self.console = Console()

    def color_string(self, string: str, color: str):
        return f"[{color}]{string}[/{color}]"

    def format_item_display(self, key: str, item: MenuItem) -> str:
        shortcut_color = ColorPicker.pickup_color(key=key, item=item)
        return f"{self.color_string(string=key,color=shortcut_color)} - {item.title}"

    def display_items(self, items: dict[str, MenuItem]) -> None:
        for key, item in items.items():
            self.console.print(
                self.format_item_display(
                    key=key,
                    item=item,
                )
            )

    def display_invalid_choice(self) -> None:
        message = "Please select available choices"
        color = ColorPicker.invalid_color
        self.console.print(self.color_string(string=message, color=color))

    def display_choice_asking(self) -> str:
        message = "Sélectionner une action : "
        color = ColorPicker.input_awaiting_color
        return self.console.input(
            self.color_string(string=message, color=color)
        ).upper()
