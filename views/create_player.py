from __future__ import annotations

from config.view_constants import BACK_SHORTCUT
from controllers.create_player import CreatePlayerAction
from controllers.choice import Choice, Choices
from repository.player_repository import PlayerRepository

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.renderer import Renderer
    from repository.data import DataRepository


class PlayerView:

    def __init__(self, repository: DataRepository, choices: Choices) -> None:
        self.repository = repository
        self.choices = choices

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
                renderer=renderer,
            )

        return user_choice


def player_view_builder() -> PlayerView:
    repository = PlayerRepository()

    create_player = Choice(
        title="Create player",
        shortcut="CP",
        action=CreatePlayerAction(repository=repository),
    )
    go_back = Choice(
        title="Go back",
        shortcut=BACK_SHORTCUT,
    )

    choices = Choices(
        [
            create_player,
            go_back,
        ]
    )

    view = PlayerView(repository=repository, choices=choices)
    return view
