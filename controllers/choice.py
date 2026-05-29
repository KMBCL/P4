from __future__ import annotations

from dataclasses import dataclass, field

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.action import Action


@dataclass
class Choice:
    title: str
    shortcut: str
    action: Action | None = None
    view: str = "Set choice view as actual"


@dataclass
class Choices:
    choices: list[Choice] = field(default_factory=list["Choice"])

    def get_choice_by_shortcut(self, shortcut: str) -> Choice | None:
        for choice in self.choices:
            if choice.shortcut == shortcut:
                return choice
        return None

    def validate_user_choice(self, user_choice: Choice):
        return user_choice in self.choices
