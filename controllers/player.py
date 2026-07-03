from models.player import Player
from service.player import PlayerService
from controllers.handlers.player import PlayerPromptHandler, PlayerRenderHandler


class PlayerController:
    def __init__(
        self,
        prompt_handler: PlayerPromptHandler,
        renderer_handler: PlayerRenderHandler,
        player_service: PlayerService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.player_service = player_service

    def create_new_player(self) -> None:
        user_input = self.prompt_handler.get_player_input()
        create_result = self.player_service.create_new_player(user_input)
        if not create_result:
            self.renderer_handler.view.render_invalid_input(create_result.get_reason())
            return None

        self.renderer_handler.view.render_success(create_result.get_success_message())

    def show_players(self) -> None:
        players_result = self.player_service.get_players()
        if not players_result:
            self.renderer_handler.view.render_invalid_input(players_result.get_reason())
            return None

        players: list[Player] = players_result.get_value()
        self.renderer_handler.render_players(players)
