from __future__ import annotations

from dataclasses import fields, Field
from typing import TYPE_CHECKING, Any, Generic, TypeVar
from enum import Enum

from core.core_model import Model
from models.menu import MenuItem

if TYPE_CHECKING:
    from rich.console import Console


TModel = TypeVar("TModel", bound=Model[Any])


class ListView:

    def __init__(self, console: Console) -> None:
        self.console = console

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

    def prompt_menu_choice(self) -> str:
        return self.console.input("Select key menu : ")

    def render_menu_items(self, menu_items: list[MenuItem]):
        MENU_START = 1
        menu_key = MENU_START
        for menu_item in menu_items:
            displayed = f"{menu_key} - {menu_item.title}"
            self.console.print(displayed)
            menu_key += 1


class CoreView(Generic[TModel]):

    def __init__(self, console: Console) -> None:
        self.console = console
        self.list_view = ListView(console)

    def prompt_action(self) -> str:
        return self.console.input("Select choice : ").upper()

    def render_invalid_input(self, reason: str) -> None:
        self.console.print(f"[red]{reason}[/red]")

    def render_success(self, success_message: str) -> None:
        self.console.print(f"[green]{success_message}[/green]")
