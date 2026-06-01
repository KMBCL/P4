from __future__ import annotations

from typing import TYPE_CHECKING

from controllers.style import StylePicker

if TYPE_CHECKING:
    from rich.console import Console

    from controllers.choice import Choice
    from repository.data import DataItem, DataSet


class Renderer:

    def __init__(self, console: Console) -> None:
        self.console = console

    def style_string(self, string: str, style: str) -> str:
        return f"[{style}]{string}[/]"

    def format_choice_display(self, choice: Choice) -> str:
        shortcut_style: str = StylePicker.pickup_style(choice=choice)
        return f"{self.style_string(string=choice.shortcut,style=shortcut_style)} - {choice.title}"

    def render_choices(self, choices: list[Choice]):
        for choice in choices:
            self.console.print(
                self.format_choice_display(
                    choice=choice,
                )
            )

    def render_invalid_choice(self) -> None:
        message: str = "Please select available choices"
        style: str = StylePicker.invalid_style
        self.console.print(self.style_string(string=message, style=style))

    def render_choice_input(self) -> str:
        message: str = "Type selected choice here : "
        style: str = StylePicker.input_awaiting_style
        return self.console.input(
            self.style_string(string=message, style=style)
        ).upper()

    def format_data_display(self, data_item: DataItem) -> str:
        shortcut_style: str = StylePicker.navigation_style
        return f"{self.style_string(string=data_item.shortcut,style=shortcut_style)} - {data_item.content}"

    def render_data(self, data_set: DataSet) -> None:
        for data_item in data_set.data_items:
            self.console.print(self.format_data_display(data_item=data_item))

    def render_step(self, step: str) -> str:
        style: str = StylePicker.input_awaiting_style
        return self.console.input(self.style_string(string=step, style=style))
