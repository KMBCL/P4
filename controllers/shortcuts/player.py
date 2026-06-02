from __future__ import annotations

from enum import Enum

from controllers.shortcuts.core_shortcuts import CoreShortcut, ShortcutDefinition


class PlayerShortcut(Enum):
    CREATE_PLAYER = ShortcutDefinition(
        shortcut="CP",
        full_label="Create new player",
    )
    PLAYERS = ShortcutDefinition(
        shortcut="PS",
        full_label="Show all players",
    )
    BACK = CoreShortcut.BACK.value
