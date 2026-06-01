from __future__ import annotations

from typing import TYPE_CHECKING

from views.view_path import ViewPath

if TYPE_CHECKING:
    from views.view import View


class ViewRegistry:

    def __init__(self) -> None:
        self.registry: dict[ViewPath, View] = {}

    def register_view(self, view_path: ViewPath, view: View) -> None:
        self.registry[view_path] = view

    def get_view(self, view_path: ViewPath) -> View | None:
        view = self.registry.get(view_path)
        return view

    def get_required_view(self, view_path: ViewPath) -> View:
        view = self.registry.get(view_path)
        if view is None:
            raise ValueError(f"no required view for {view_path} view path")
        return view


VIEW_REGISTRY = ViewRegistry()
