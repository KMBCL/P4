from typing import Any

from core.core_view import CoreView


class CoreRenderer:

    def __init__(self, view: CoreView[Any]) -> None:
        self.view = view

    def render_undefined_action(self, action: str) -> None:
        self.view.render_invalid_input(
            reason=f"{action} shortcut exists, but no action handled"
        )

    def render_ignored_kwargs(self, action_kwargs: Any) -> None:
        self.view.render_invalid_input(
            reason=f"Action done, but with unexpected kwargs : {action_kwargs}. Kwargs ignored"
        )
