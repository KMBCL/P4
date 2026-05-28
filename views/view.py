from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ViewDefinition:
    title: str
    shortcut: str


@dataclass
class View:
    title: str
    shortcut: str
    parent_view: View | None = None
    child_views: list[View] = field(default_factory=list["View"])

    def set_parent_view(self, parent_view: View) -> None:
        self.parent_view = parent_view

    def build_child_view(self, child_definition: ViewDefinition) -> View:
        return View(
            title=child_definition.title,
            shortcut=child_definition.shortcut,
            parent_view=self,
        )

    def add_child_definitions(self, child_definitions: list[ViewDefinition]) -> None:
        for child_definition in child_definitions:
            new_child_view = self.build_child_view(child_definition)
            self.child_views.append(new_child_view)

    def add_child_views(self, child_views: list[View]) -> None:
        for child_view in child_views:
            child_view.set_parent_view(self)
            self.child_views.append(child_view)

    def back_item(self) -> dict[str, View] | None:
        if self.parent_view is None:
            return None

        return {"B": self.parent_view}

    def build_view_tree(self) -> dict[str, View]:
        tree: dict[str, View] = {}

        for child_view in self.child_views:
            tree[child_view.shortcut] = child_view

        back_item = self.back_item()
        if back_item:
            tree.update(**back_item)

        return tree

    def build_context(self) -> dict[Any, Any]:
        context: dict[Any, Any] = {}
        context["navigation"] = self.build_view_tree()

        return context

    def get_related_view(self, shortcut: str) -> View | None:
        tree = self.build_view_tree()
        view = tree.get(shortcut, None)
        return view
