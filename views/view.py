from __future__ import annotations

from controllers.choice import Choice, Choices

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.renderer import Renderer
    from repository.data import DataRepository, DataSet


class View:

    def __init__(
        self, choices: Choices, repository: DataRepository | None = None
    ) -> None:
        self.repository = repository
        self.choices = choices

    def get_data(self) -> DataSet | None:
        if self.repository is None:
            return None

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
