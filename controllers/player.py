from typing import Any

from core.core_controller import CoreController
from repository.player import PlayerRepository
from controllers.handlers.player import PlayerPromptHandler, PlayerRenderHandler


class PlayerController(
    CoreController[
        PlayerRepository,
        PlayerPromptHandler,
        PlayerRenderHandler,
    ]
):

    def create_new_player(self) -> None:
        self.repository.save_new_model(
            user_input=self.prompt_handler.get_player_input()
        )

    def show_players(self) -> None:
        players = self.repository.get_models()
        self.renderer_handler.render_players(players)

    def show_player(self, pk: str) -> None:
        player = self.repository.get_model(key="pk", value=pk)
        if player is None:
            return None

        self.renderer_handler.render_players([player])

    def show_filtered_players(self, **kwargs: Any) -> None:
        if not kwargs:
            return

        filtered_players = self.repository.get_filtered_models(filters=kwargs)
        self.renderer_handler.render_players(filtered_players)
