from __future__ import annotations

from dataclasses import dataclass, field

from typing import TYPE_CHECKING, Any
from enum import StrEnum


from config.view_constants import EXIT_SHORTCUT, BACK_SHORTCUT

if TYPE_CHECKING:
    from controllers.action import Action
    from views.view_path import ViewPath


class ChoiceStyleKey(StrEnum):
    EXIT = "exit"
    BACK = "back"
    ACTION = "action"
    NAVIGATION = "navigation"


@dataclass
class Choice:
    title: str
    shortcut: str
    action: Action[Any] | None = None
    view_path: ViewPath | None = None

    @property
    def style_to_apply(self) -> ChoiceStyleKey:
        if self.shortcut == EXIT_SHORTCUT:
            return ChoiceStyleKey.EXIT

        if self.shortcut == BACK_SHORTCUT:
            return ChoiceStyleKey.BACK

        if self.action is not None:
            return ChoiceStyleKey.ACTION

        return ChoiceStyleKey.NAVIGATION


def default_choices() -> list[Choice]:
    return []


@dataclass
class Choices:
    choices: list[Choice] = field(default_factory=default_choices)

    def get_choice_by_shortcut(self, shortcut: str) -> Choice | None:
        for choice in self.choices:
            if choice.shortcut == shortcut:
                return choice
        return None

    def validate_user_choice(self, user_choice: Choice):
        return user_choice in self.choices
