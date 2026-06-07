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
    REGISTERED_PLAYERS = ShortcutDefinition(
        shortcut="SP",
        full_label="Show selected tournament registered players",
    )
    REGISTER_PLAYER = ShortcutDefinition(
        shortcut="RP",
        full_label="Register player to tournament",
    )

    FILTER_TOURNAMENTS = ShortcutDefinition(
        shortcut="FT",
        full_label="Filter tournaments (ex : 'FP:place=somewhere')",
    )
    TOURNAMENT_ROUNDS = ShortcutDefinition(
        shortcut="TR",
        full_label="Show selected tournament rounds",
    )
    SET_ROUND_MATCHES = ShortcutDefinition(
        shortcut="SM", full_label="Set round matches"
    )
    BACK = CoreShortcut.BACK.value
