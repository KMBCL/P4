from __future__ import annotations
from typing import TYPE_CHECKING

from config.menu_constants import EXIT_SHORTCUT, BACK_SHORTCUT

from rich.console import Console

if TYPE_CHECKING:
    from models.menu_item import MenuItem


class StylePicker:
    exit_style = "bold red"
    back_style = "bold yellow"
    navigation_style = "bold cyan"
    action_style = "bold green"
    invalid_style = "red"
    input_awaiting_style = "green"

    @classmethod
    def pickup_style(cls, key: str, item: MenuItem) -> str:
        if key == EXIT_SHORTCUT:
            return cls.exit_style

        if key == BACK_SHORTCUT:
            return cls.back_style

        if not item.child_items:
            return cls.action_style

        return cls.navigation_style


class MenuDisplay:

    def __init__(self) -> None:
        self.console = Console()

    def style_string(self, string: str, style: str) -> str:
        return f"[{style}]{string}[/]"

    def format_item_display(self, key: str, item: MenuItem) -> str:
        shortcut_style = StylePicker.pickup_style(key=key, item=item)
        return f"{self.style_string(string=key,style=shortcut_style)} - {item.title}"

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
        style = StylePicker.invalid_style
        self.console.print(self.style_string(string=message, style=style))

    def display_choice_asking(self) -> str:
        message = "Sélectionner une action : "
        style = StylePicker.input_awaiting_style
        return self.console.input(
            self.style_string(string=message, style=style)
        ).upper()
