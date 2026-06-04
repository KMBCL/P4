from typing import Any

from rich.console import Console

from core.core_controller import CoreController

from view.player import PlayerView

from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.handlers.player import PlayerPromptHandler, PlayerRenderHandler
from controllers.shortcuts.player import PlayerShortcut
from controllers.menu_state import MenuState

from repository.player import PlayerRepository


class PlayerController(CoreController):

    def __init__(self, console: Console) -> None:
        view: PlayerView = PlayerView(console=console)
        self.repository = PlayerRepository()
        self.prompt_handler = PlayerPromptHandler(view=view)
        self.render_controller = PlayerRenderHandler(view=view)

        action_runner = ActionRunner(
            target_controller=self,
            action_routing=ACTION_ROUTING,
            prompt_handler=self.prompt_handler,
            render_controller=self.render_controller,
        )

        super().__init__(action_runner=action_runner)

    def create_new_player(self) -> None:
        self.repository.save_new_player(
            player_input=self.prompt_handler.get_player_input()
        )

    def show_players(self) -> None:
        players = self.repository.get_players()
        self.render_controller.render_players(players)

    def show_player(self, pk: str) -> None:
        player = self.repository.get_player_by_pk(pk)
        if player is None:
            return None

        self.render_controller.render_players([player])

    def show_filtered_players(self, **kwargs: Any) -> None:
        if not kwargs:
            return

        filtered_players = self.repository.get_filtered_players(filters=kwargs)
        self.render_controller.render_players(filtered_players)


ACTION_ROUTING: ActionRouting = {
    PlayerShortcut.CREATE_PLAYER.value.shortcut: PlayerController.create_new_player,
    PlayerShortcut.PLAYERS.value.shortcut: PlayerController.show_players,
    PlayerShortcut.SELECT_PLAYER.value.shortcut: PlayerController.show_player,
    PlayerShortcut.FILTER_PLAYER.value.shortcut: PlayerController.show_filtered_players,
    PlayerShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
