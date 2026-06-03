from __future__ import annotations

from enum import Enum

from core.core_shortcuts import CoreShortcut, ShortcutDefinition


class PlayerShortcut(Enum):
    CREATE_PLAYER = ShortcutDefinition(
        shortcut="CP",
        full_label="Create new player",
    )
    PLAYERS = ShortcutDefinition(
        shortcut="PS",
        full_label="Show all players",
    )
    SELECT_PLAYER = ShortcutDefinition(
        shortcut="PD",
        full_label="Select player (ex : 'PD:pk=1')",
        kwargs=["pk"],
    )
    FILTER_PLAYER = ShortcutDefinition(
        shortcut="FP",
        full_label="Filter players (ex : 'FP:last_name=iron')",
        kwargs=["field_name", "field_value"],
    )
    BACK = CoreShortcut.BACK.value
