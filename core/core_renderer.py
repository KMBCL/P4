"""Provides the base every render handler is built on."""

from typing import Any

from core.core_view import CoreView


class CoreRenderer:
    """Bases a render handler, holding the view it prints through."""

    def __init__(self, view: CoreView[Any]) -> None:
        """Holds the view the handler prints through.

        Args:
            view (CoreView[Any]): The view to print through.
        """
        self.view = view

    def to_green(self, value: str) -> str:
        """Colours a value in green.

        Args:
            value (str): The value to colour.

        Returns:
            str: The coloured value.
        """
        return f"[green]{value}[/green]"
