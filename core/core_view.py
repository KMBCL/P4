from __future__ import annotations

from dataclasses import fields, Field
from typing import TYPE_CHECKING, Any, Generic
from enum import Enum

from core.core_model import TModel

if TYPE_CHECKING:
    from rich.console import Console

    from core.core_shortcuts import ShortcutDefinition


class CoreView(Generic[TModel]):

    def __init__(self, console: Console) -> None:
        self.console: Console = console

    def render_available_actions(self, action_shortcuts: type[Enum]) -> None:
        self.console.print("Select : ")
        for member in action_shortcuts:
            shortcut_definition: ShortcutDefinition = member.value
            self.console.print(
                f"{shortcut_definition.shortcut} - {shortcut_definition.full_label}"
            )

    def prompt_action(self) -> str:
        return self.console.input("Select choice : ").upper()

    def format_field(self, model: TModel, field: Field[Any]) -> str:
        return f"{field.name}={getattr(model,field.name)}"

    def format_model(self, model: TModel) -> str:
        formatted_fields = [self.format_field(model, field) for field in fields(model)]
        return " - ".join(formatted_fields)

    def render_models(self, models: list[TModel]):
        for model in models:
            formatted_player = self.format_model(model)
            self.console.print(formatted_player)
        self.console.print(f"total : {len(models)}")

    def render_invalid_input(self, reason: str) -> None:
        self.console.print(reason)
