from dataclasses import dataclass, field

from enum import Enum


def default_kwargs() -> list[str]:
    return []


@dataclass
class ShortcutDefinition:
    shortcut: str
    full_label: str
    kwargs: list[str] = field(default_factory=default_kwargs)


class CoreShortcut(Enum):
    EXIT = ShortcutDefinition(
        shortcut="E",
        full_label="Exit",
    )
    BACK = ShortcutDefinition(
        shortcut="B",
        full_label="Back",
    )
