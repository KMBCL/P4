"""Provides the menu tree, built from the menu definition stored as JSON."""

from __future__ import annotations

from typing import Any, Self
from dataclasses import dataclass, field


def default_sub_menus() -> list[MenuItem]:
    """Builds the default sub menus of a menu item.

    Returns:
        list[MenuItem]: An empty list.
    """
    sub_menus: list[MenuItem] = []
    return sub_menus


@dataclass
class MenuItem:
    """Represents one entry of the menu, and the entries nested under it.

    An item either navigates, when it holds sub menus, or triggers an action.
    """

    code: str
    title: str
    value: Any | None = None
    sub_menus: list[MenuItem] = field(default_factory=default_sub_menus)

    @classmethod
    def from_json(cls, json_dict: dict[str, Any]) -> Self:
        """Builds a menu item and every item nested under it.

        Args:
            json_dict (dict[str, Any]): The raw definition of the item.

        Returns:
            Self: The item, with its sub menus built recursively.
        """
        menu_item = cls(
            code=json_dict["code"],
            title=json_dict["title"],
            sub_menus=[
                MenuItem.from_json(sub_menu) for sub_menu in json_dict["sub_menus"]
            ],
        )
        return menu_item

    def __repr__(self) -> str:
        """Represents the item by its code alone.

        Returns:
            str: The code of the item.
        """
        return self.code


@dataclass
class MenuStructure:
    """Holds the whole menu, from the item the user is shown first."""

    root_item: MenuItem

    @classmethod
    def from_json(cls, json_data: list[dict[str, Any]]) -> Self:
        """Builds the menu from its stored definition.

        The definition is stored as a list, the menu has a single root.

        Args:
            json_data (list[dict[str, Any]]): The raw definition of the menu.

        Returns:
            Self: The menu, built from the first definition of the list.
        """
        menu_structure = [cls(root_item=MenuItem.from_json(data)) for data in json_data]
        return menu_structure[0]
