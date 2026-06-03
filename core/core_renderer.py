from typing import Any

from core.core_view import CoreView


class CoreRenderer:

    def __init__(self, view: CoreView[Any]):
        self.view = view

    def render_undefined_action(self, action: str):
        self.view.render_invalid_input(
            reason=f"{action} shortcut exists, but no action handled"
        )
