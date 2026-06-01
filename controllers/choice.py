from __future__ import annotations

from dataclasses import dataclass, field

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from controllers.action import Action
    from views.view_path import ViewPath


@dataclass
class Choice:
    title: str
    shortcut: str
    action: Action[Any] | None = None
    view_path: ViewPath | None = None


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
