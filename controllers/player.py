from typing import Any


from service.player import PlayerService
from controllers.handlers.player import PlayerPromptHandler, PlayerRenderHandler


class PlayerController:
    def __init__(
        self,
        prompt_handler: PlayerPromptHandler,
        renderer_handler: PlayerRenderHandler,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.service = PlayerService()

    def create_new_player(self) -> None:
        self.service.repository.save_new_model(
            user_input=self.prompt_handler.get_player_input()
        )

    def show_players(self) -> None:
        players = self.service.repository.get_models()
        self.renderer_handler.render_players(players)

    def show_player(self, pk: str) -> None:
        player = self.service.repository.get_model(key="pk", value=pk)
        if player is None:
            return None

        self.renderer_handler.render_players([player])

    def show_filtered_players(self, **kwargs: Any) -> None:
        if not kwargs:
            return

        filtered_players = self.service.repository.get_filtered_models(filters=kwargs)
        self.renderer_handler.render_players(filtered_players)
