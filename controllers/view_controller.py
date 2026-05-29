from __future__ import annotations

from typing import TYPE_CHECKING

from views.create_player import View
from repository.data import DataRepository

if TYPE_CHECKING:
    from controllers.renderer import Renderer
    from controllers.choice import Choices
    from repository.data import DataSet


class ViewController:

    actual_view: View

    def __init__(
        self,
        renderer: Renderer,
    ):
        self.actual_view = View()
        self.renderer = renderer
        self.fake_repository = DataRepository()

    def run(self) -> None:
        exit = False

        while not exit:

            choices: Choices = self.actual_view.build_choices()
            data_set: DataSet = self.actual_view.get_data()

            self.renderer.render_data(data_set)
            self.renderer.render_choices(choices.choices)
            user_choice_shortcut = self.renderer.render_choice_input()
            user_choice = choices.get_choice_by_shortcut(user_choice_shortcut)

            if user_choice is None or not choices.validate_user_choice(user_choice):
                self.renderer.render_invalid_choice()
                continue

            if user_choice.action:
                user_choice.action.run(
                    fake_repository=self.fake_repository,
                    renderer=self.renderer,
                )

            print(user_choice.view)
