from enum import Enum

from core.core_shortcuts import CoreShortcut, ShortcutDefinition


class MainShortcut(Enum):
    HANDLE_PLAYERS = ShortcutDefinition(
        shortcut="HP",
        full_label="Handle players",
    )
    HANDLE_TOURNAMENTS = ShortcutDefinition(
        shortcut="HT",
        full_label="Handle tournaments",
    )
    EXIT = CoreShortcut.EXIT.value
