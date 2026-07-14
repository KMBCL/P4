"""Provides the menu codes reserved by the navigation."""

from enum import StrEnum


class MenuCode(StrEnum):
    """Codes the menu answers itself, rather than by running an action."""

    EXIT = "exit"
    BACK = "back"
