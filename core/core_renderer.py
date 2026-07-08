from typing import Any

from core.core_view import CoreView


class CoreRenderer:

    def __init__(self, view: CoreView[Any]) -> None:
        self.view = view

    def to_green(self, value: str) -> str:
        return f"[green]{value}[/green]"
