from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from controllers.action import Action
from models.player import Player, PlayerInputData

if TYPE_CHECKING:
    from repository.player_repository import PlayerRepository
    from controllers.renderer import Renderer


class CreatePlayerAction(Action):

    def input_new_player(self, renderer: Renderer) -> PlayerInputData:
        chess_id: str = renderer.render_step("Enter chess id : ")
        last_name: str = renderer.render_step("Enter last name : ")
        first_name: str = renderer.render_step("Enter first name : ")

        player_input = PlayerInputData(
            chess_id=chess_id,
            last_name=last_name,
            first_name=first_name,
        )
        return player_input

    def build_new_player(self, player_input: PlayerInputData, new_pk: int):

        new_player = Player.from_player_input(new_pk=new_pk, player_input=player_input)
        return new_player

    def make_new_pk(self, repository: PlayerRepository):
        new_pk = len(repository.get_players()) + 1
        return new_pk

    def run(
        self,
        repository: PlayerRepository,
        renderer: Renderer,
    ) -> None:
        player_input = self.input_new_player(renderer)
        new_pk = self.make_new_pk(repository=repository)
        player = self.build_new_player(
            player_input=player_input,
            new_pk=new_pk,
        )
        repository.write_data(json_data=player.to_json())
