from enum import Enum

from core.core_shortcuts import CoreShortcut, ShortcutDefinition


class TournamentShortcut(Enum):
    CREATE_TOURNAMENT = ShortcutDefinition(
        shortcut="CT",
        full_label="Create new tournament",
    )
    TOURNAMENTS = ShortcutDefinition(
        shortcut="TS",
        full_label="Show all tournaments",
    )
    REGISTER_PLAYER = ShortcutDefinition(
        shortcut="RP",
        full_label="Register player to tournament",
    )

    FILTER_TOURNAMENTS = ShortcutDefinition(
        shortcut="FT",
        full_label="Filter tournaments (ex : 'FP:place=somewhere')",
        kwargs=["field_name", "field_value"],
    )
    BACK = CoreShortcut.BACK.value
