from __future__ import annotations
from dataclasses import dataclass

from rich.console import Console


@dataclass
class PlayerInputData:
    chess_id: str
    last_name: str
    first_name: str


class PlayerDisplay:

    def __init__(self, console: Console) -> None:
        self.console = console

    def display_create_player(self) -> PlayerInputData:
        chess_id: str = self.console.input("Enter chess id : ")
        last_name: str = self.console.input("Enter last name : ")
        first_name: str = self.console.input("Enter first name : ")
        new_player = PlayerInputData(
            chess_id=chess_id,
            last_name=last_name,
            first_name=first_name,
        )
        return new_player
