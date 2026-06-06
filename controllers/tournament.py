from __future__ import annotations

from typing import TYPE_CHECKING

from core.core_controller import CoreController

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from repository.tournament import TournamentRepository

from view.player import PlayerView
from view.round import RoundView


class TournamentController(
    CoreController[
        TournamentRepository,
        TournamentPromptHandler,
        TournamentRenderHandler,
    ]
):

    def create_new_tournament(self) -> None:
        self.repository.save_new_model(
            user_input=self.prompt_handler.get_tournament_input()
        )

    def register_player(self) -> None:
        user_input = self.prompt_handler.get_player_registration_input()
        result = self.repository.register_player_to_tournament(
            tournament_pk=int(user_input.tournament_pk),
            chess_id=user_input.chess_id,
        )

        if not result:
            self.renderer_handler.view.render_invalid_input(
                reason=result.required_reason
            )

    def show_tournaments(self) -> None:
        tournaments = self.repository.get_models()
        self.renderer_handler.render_tournaments(tournaments)

    def show_filtered_tournaments(self) -> None:
        pass

    def show_tournament_players(self) -> None:
        user_input = self.prompt_handler.get_tournament_pk_input()
        registered_players = self.repository.get_registered_players(
            tournament_pk=int(user_input)
        )

        player_view = PlayerView(console=self.renderer_handler.view.console)
        player_view.render_models(registered_players)

    def show_tournament_rounds(self) -> None:
        user_input = self.prompt_handler.get_tournament_pk_input()
        result = self.repository.get_tournament_rounds(tournament_pk=int(user_input))
        if not result:
            self.renderer_handler.view.render_invalid_input(
                reason=result.required_reason
            )

        tournament_rounds = result.required_value
        round_view = RoundView(console=self.renderer_handler.view.console)
        round_view.render_models(tournament_rounds)
