from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from repository.data import DataItem
from controllers.action import Action

if TYPE_CHECKING:
    from repository.data import DataRepository
    from controllers.renderer import Renderer


@dataclass
class PlayerInputData:
    chess_id: str
    last_name: str
    first_name: str

    def serialize_data(self) -> str:
        serialized_data = f"chess_id={self.chess_id}, last_name={self.last_name}, first_name={self.first_name}"
        return serialized_data


class CreatePlayerAction(Action):

    def input_new_player(self, renderer: Renderer) -> PlayerInputData:
        chess_id: str = renderer.render_step("Enter chess id : ")
        last_name: str = renderer.render_step("Enter last name : ")
        first_name: str = renderer.render_step("Enter first name : ")

        new_player = PlayerInputData(
            chess_id=chess_id,
            last_name=last_name,
            first_name=first_name,
        )
        return new_player

    def run(
        self,
        fake_repository: DataRepository,
        renderer: Renderer,
    ) -> None:
        new_player = self.input_new_player(renderer)
        fake_repository.write_data(new_player.serialize_data())
