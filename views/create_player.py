from __future__ import annotations

from config.view_constants import BACK_SHORTCUT
from controllers.create_player import CreatePlayerAction
from controllers.choice import Choice, Choices
from repository.player_repository import PlayerRepository

from repository.data import DataSet, INITIAL_DATA_SET

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.renderer import Renderer

CHOICES = [
    Choice(title="Create player", shortcut="CP", action=CreatePlayerAction()),
    Choice(title="Go back", shortcut=BACK_SHORTCUT),
]


class PlayerView:

    def __init__(self) -> None:
        self.repository = PlayerRepository()
        self.choices = Choices(CHOICES)

    def get_data(self):
        data_set = self.repository.get_data()
        return data_set

    def get_choices(self) -> Choices:
        return self.choices

    def run_choice(
        self, user_choice_shortcut: str, renderer: Renderer
    ) -> Choice | None:
        user_choice = self.choices.get_choice_by_shortcut(user_choice_shortcut)

        if user_choice is None or not self.choices.validate_user_choice(user_choice):
            return None

        if user_choice.action:
            user_choice.action.run(
                repository=self.repository,
                renderer=renderer,
            )

        return user_choice
