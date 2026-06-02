from __future__ import annotations

from dataclasses import fields, Field
from typing import TYPE_CHECKING, Any, Generic

from models.core_model import TModel

if TYPE_CHECKING:
    from rich.console import Console


class CoreView(Generic[TModel]):

    def __init__(self, console: Console) -> None:
        self.console: Console = console

    def render_available_actions(self) -> None: ...

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
