from enum import Enum

from core.core_shortcuts import CoreShortcut, ShortcutDefinition


class PlayerTournamentShortcut(Enum):
    ADD_PLAYER_TO_TOURNAMENT = ShortcutDefinition(
        shortcut="PT",
        full_label="Add player to tournament",
    )
    BACK = CoreShortcut.BACK.value
