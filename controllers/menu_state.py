"""Provides the answer an action gives to the menu loop."""

from __future__ import annotations


class MenuState:
    """Tells the menu loop if to keep running."""

    def __init__(self, should_continue: bool) -> None:
        """Holds the answer given to the menu loop.

        Args:
            should_continue (bool): if the loop keeps running.
        """
        self.should_continue: bool = should_continue

    @classmethod
    def continue_loop(cls) -> MenuState:
        """Keeps the menu loop running.

        Returns:
            MenuState: The state keeping the loop running.
        """
        return MenuState(should_continue=True)

    @classmethod
    def break_loop(cls) -> MenuState:
        """Stops the menu loop.

        Returns:
            MenuState: The state stopping the loop.
        """
        return MenuState(should_continue=False)

    def __bool__(self):
        """Tells if the menu loop keeps running.

        Returns:
            bool: True when the loop keeps running.
        """
        return self.should_continue
