from __future__ import annotations

from typing import Any, Self
from dataclasses import dataclass, field


def default_sub_menus() -> list[MenuItem]:
    sub_menus: list[MenuItem] = []
    return sub_menus


@dataclass
class MenuItem:
    code: str
    title: str
    value: Any | None = None
    sub_menus: list[MenuItem] = field(default_factory=default_sub_menus)

    @classmethod
    def from_json(cls, json_dict: dict[str, Any]) -> Self:
        menu_item = cls(
            code=json_dict["code"],
            title=json_dict["title"],
            sub_menus=[
                MenuItem.from_json(sub_menu) for sub_menu in json_dict["sub_menus"]
            ],
        )
        return menu_item

    def __repr__(self) -> str:
        return self.code


@dataclass
class MenuStructure:
    root_item: MenuItem

    @classmethod
    def from_json(cls, json_data: list[dict[str, Any]]) -> Self:
        menu_structure = [cls(root_item=MenuItem.from_json(data)) for data in json_data]
        return menu_structure[0]
