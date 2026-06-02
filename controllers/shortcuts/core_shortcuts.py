from dataclasses import dataclass

from enum import Enum


@dataclass
class ShortcutDefinition:
    shortcut: str
    full_label: str


class CoreShortcut(Enum):
    EXIT = ShortcutDefinition(
        shortcut="E",
        full_label="Exit",
    )
    BACK = ShortcutDefinition(
        shortcut="B",
        full_label="Back",
    )
