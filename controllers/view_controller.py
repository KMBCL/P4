from __future__ import annotations
from typing import TYPE_CHECKING

from views.view import View
from config.view_constants import EXIT_SHORTCUT

if TYPE_CHECKING:
    from controllers.view_renderer import ViewRenderer


class ViewControler:
    actual_view: View

    def __init__(
        self,
        root_view: View,
        view_renderer: ViewRenderer,
    ):
        self.actual_view = root_view
        self.view_renderer = view_renderer

    def run_view(self) -> None:
        exit = False

        while not exit:

            self.view_renderer.render_view(self.actual_view)
            user_choice = self.view_renderer.render_navigation_asking()
            selected_view = self.actual_view.get_related_view(user_choice)

            if selected_view is None:
                self.view_renderer.render_invalid_choice()
                continue

            if selected_view.shortcut == EXIT_SHORTCUT:
                exit = True
                continue

            self.actual_view = selected_view
