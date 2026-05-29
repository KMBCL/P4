from __future__ import annotations

from typing import TYPE_CHECKING

from views.create_player import player_view_builder
from repository.data import DataRepository

if TYPE_CHECKING:
    from controllers.renderer import Renderer
    from controllers.choice import Choices
    from repository.data import DataSet


class ViewController:

    def __init__(
        self,
        renderer: Renderer,
    ):
        self.actual_view = player_view_builder()
        self.renderer = renderer

    def run(self) -> None:
        exit = False

        while not exit:

            choices: Choices = self.actual_view.get_choices()
            data_set: DataSet = self.actual_view.get_data()

            self.renderer.render_data(data_set)
            self.renderer.render_choices(choices.choices)

            user_choice_shortcut = self.renderer.render_choice_input()
            user_choice = self.actual_view.run_choice(
                user_choice_shortcut=user_choice_shortcut,
                renderer=self.renderer,
            )

            if user_choice is None:
                self.renderer.render_invalid_choice()
                continue

            print(user_choice.view)
