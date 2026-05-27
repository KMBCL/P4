from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.menu_item import MenuItem


class MenuDisplay:

    def display_items(self, items: dict[str, MenuItem]) -> None:
        for shortcut, item in items.items():
            print(f"{shortcut} - {item.title}")

    def display_invalid_choice(self) -> None:
        print("Please select available choices")

    def display_choice_asking(self) -> str:
        return input("Sélectionner une action : ").upper()
