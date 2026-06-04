from enum import Enum

from core.core_shortcuts import CoreShortcut, ShortcutDefinition


class PlayerRegistrationShortcut(Enum):
    REGISTER_PLAYER = ShortcutDefinition(
        shortcut="RP",
        full_label="Register player to tournament",
    )
    BACK = CoreShortcut.BACK.value
