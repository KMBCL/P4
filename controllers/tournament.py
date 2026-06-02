from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from controllers.action import Action
from models.tournament import Tournament, TournamentInputData
from repository.tournament import TournamentRepository

if TYPE_CHECKING:

    from views.renderer import Renderer


class CreatePTournamentAction(Action[TournamentRepository]):

    def build_new(self, user_input: TournamentInputData, new_pk: int):
        new = Tournament.from_user_input(new_pk=new_pk, user_input=user_input)
        return new

    def make_new_pk(self, repository: TournamentRepository):
        new_pk = repository.get_data().new_pk()
        return new_pk

    def run(
        self,
        renderer: Renderer,
    ) -> None:
        user_input = self.input_new(renderer)
        new_pk = self.make_new_pk(repository=self.repository)
        player = self.build_new(
            user_input=user_input,
            new_pk=new_pk,
        )
        self.repository.write_data(json_data=player.to_json())
