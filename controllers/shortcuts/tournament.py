from enum import StrEnum, Enum
from controllers.shortcuts.core_shortcuts import CoreShortcut, ShortcutDefinition


class TournamentShortcut(Enum):
    CREATE_TOURNAMENT = ShortcutDefinition(
        shortcut="CT",
        full_label="Create new tournament",
    )
    TOURNAMENTS = ShortcutDefinition(
        shortcut="TS",
        full_label="Show all tournaments",
    )
    BACK = CoreShortcut.BACK.value
