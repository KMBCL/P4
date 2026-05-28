from __future__ import annotations
from typing import TYPE_CHECKING

from config.view_constants import EXIT_SHORTCUT, BACK_SHORTCUT

if TYPE_CHECKING:
    from views.view import View
    from rich.console import Console


class StylePicker:
    exit_style = "bold red"
    back_style = "bold yellow"
    navigation_style = "bold cyan"
    action_style = "bold green"
    invalid_style = "red"
    input_awaiting_style = "green"

    @classmethod
    def pickup_style(cls, key: str, view: View) -> str:
        if key == EXIT_SHORTCUT:
            return cls.exit_style

        if key == BACK_SHORTCUT:
            return cls.back_style

        if not view.child_views:
            return cls.action_style

        return cls.navigation_style


class ViewRenderer:

    def __init__(self, console: Console) -> None:
        self.console: Console = console

    def style_string(self, string: str, style: str) -> str:
        return f"[{style}]{string}[/]"

    def format_view_display(self, key: str, view: View) -> str:
        shortcut_style: str = StylePicker.pickup_style(key=key, view=view)
        return f"{self.style_string(string=key,style=shortcut_style)} - {view.title}"

    def render_navigation(self, view: View) -> None:
        context = view.build_context()
        navigation: dict[str, View] | None = context.get("navigation")
        if navigation is None:
            return None

        for key, view in navigation.items():
            self.console.print(
                self.format_view_display(
                    key=key,
                    view=view,
                )
            )

    def render_view(self, view: View) -> None:
        self.render_navigation(view=view)

    def render_invalid_choice(self) -> None:
        message: str = "Please select available choices"
        style: str = StylePicker.invalid_style
        self.console.print(self.style_string(string=message, style=style))

    def render_navigation_asking(self) -> str:
        message: str = "Type selected shortcut here : "
        style: str = StylePicker.input_awaiting_style
        return self.console.input(
            self.style_string(string=message, style=style)
        ).upper()
