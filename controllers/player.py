"""Runs the use cases of the players."""

from models.player import Player
from service.player import PlayerService
from controllers.handlers.player import PlayerPromptHandler, PlayerRendererHandler


class PlayerController:
    """Creates and shows the players."""

    def __init__(
        self,
        prompt_handler: PlayerPromptHandler,
        renderer_handler: PlayerRendererHandler,
        player_service: PlayerService,
    ) -> None:
        """Holds the handlers and the service the use cases are run with.

        Args:
            prompt_handler (PlayerPromptHandler): The handler to prompt through.
            renderer_handler (PlayerRendererHandler): The handler to print through.
            player_service (PlayerService): The rules governing the players.
        """
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.player_service = player_service

    def create_new_player(self) -> None:
        """Asks for a player, stores it, and tells the user how it went."""
        user_input = self.prompt_handler.get_player_input()
        create_result = self.player_service.create_new_player(user_input)
        if not create_result:
            self.renderer_handler.view.render_invalid_input(create_result.get_reason())
            return None

        self.renderer_handler.view.render_success(create_result.get_success_message())

    def show_players(self) -> None:
        """Prints every stored player, ordered by last name."""
        players_result = self.player_service.get_players()
        if not players_result:
            self.renderer_handler.view.render_invalid_input(players_result.get_reason())
            return None

        players: list[Player] = players_result.get_value()
        self.renderer_handler.render_players(players)
