from __future__ import annotations

from typing import TYPE_CHECKING


from repository.data import DataRepository

if TYPE_CHECKING:
    from views.view import View
    from views.registry import ViewRegistry

    from controllers.renderer import Renderer
    from controllers.choice import Choices, Choice
    from repository.data import DataSet


class ViewController:

    def __init__(
        self, renderer: Renderer, main_view: View, view_registry: ViewRegistry
    ):
        self.actual_view = main_view
        self.renderer = renderer
        self.view_registry = view_registry

    def render_choices(self) -> None:
        choices: Choices = self.actual_view.get_choices()
        self.renderer.render_choices(choices.choices)

    def render_data(self) -> None:
        data_set: DataSet | None = self.actual_view.get_data()
        if data_set is None:
            return None

        self.renderer.render_data(data_set)

    def get_user_choice(self) -> Choice | None:
        user_choice_shortcut = self.renderer.render_choice_input()

        user_choice = self.actual_view.run_choice(
            user_choice_shortcut=user_choice_shortcut,
            renderer=self.renderer,
        )

        return user_choice

    def change_view(self, user_choice: Choice) -> None:
        if user_choice.view_path is None:
            return None

        view = self.view_registry.get_required_view(view_path=user_choice.view_path)
        self.actual_view = view

    def run(self) -> None:
        exit = False

        while not exit:

            self.render_data()
            self.render_choices()

            user_choice = self.get_user_choice()

            if user_choice is None:
                self.renderer.render_invalid_choice()
                continue

            if user_choice.view_path is None:
                continue

            self.change_view(user_choice)
