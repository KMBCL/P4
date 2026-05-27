from __future__ import annotations
from dataclasses import dataclass, field

from config.menu_constants import BACK_SHORTCUT

from controllers.action import Action


@dataclass(kw_only=True)
class MenuItem:
    title: str
    shortcut: str
    action: Action | None = None
    parent_item: MenuItem | None = None
    child_items: list[MenuItem] = field(default_factory=list["MenuItem"])

    def add_child_item(self, child_item: MenuItem) -> None:
        child_item.parent_item = self
        self.child_items.append(child_item)

    def back_item(self) -> dict[str, MenuItem] | None:
        if self.parent_item is None:
            return None

        return {BACK_SHORTCUT: self.parent_item}

    def build_items(self) -> dict[str, MenuItem]:
        nodes: dict[str, MenuItem] = {}

        for node in self.child_items:
            nodes[node.shortcut] = node

        back_item = self.back_item()
        if back_item:
            nodes.update(**back_item)

        return nodes

    def run(self) -> None:
        if self.action is None:
            return None

        self.action.run()
