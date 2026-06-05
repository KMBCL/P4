from __future__ import annotations

from typing import TYPE_CHECKING

from core.core_controller import CoreController

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from repository.tournament import TournamentRepository


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

    def show_tournaments(self) -> None:
        tournaments = self.repository.get_models()
        self.renderer_handler.render_tournaments(tournaments)

    def show_filtered_tournaments(self) -> None:
        pass
