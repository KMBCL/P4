from typing import Any

from rich.console import Console

from core.core_controller import CoreController

from view.player import PlayerView

from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.shortcuts.player import PlayerShortcut
from view.handlers.player import PlayerPromptHandler, PlayerRenderHandler
from controllers.menu_state import MenuState

from models.player import Player, PlayerInputData
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

    def build_new_player(self, player_input: PlayerInputData, new_pk: int):
        new_player = Player.from_player_input(new_pk=new_pk, player_input=player_input)
        return new_player

    def get_player_input(self) -> PlayerInputData:
        return PlayerInputData(
            chess_id=self.prompt_handler.prompt_chess_id(),
            last_name=self.prompt_handler.prompt_last_name(),
            first_name=self.prompt_handler.prompt_first_name(),
            birthdate=self.prompt_handler.prompt_birthdate(),
        )

    def create_new_player(self) -> None:
        player = self.build_new_player(
            player_input=self.get_player_input(),
            new_pk=self.repository.make_new_pk(),
        )
        self.repository.write_data(json_data=player.to_json())

    def show_players(self) -> None:
        players = self.repository.get_players()
        self.render_controller.render_players(players)

    def show_player(self, pk: str) -> None:
        players = self.repository.get_players()
        for player in players:
            if player.pk == int(pk):
                self.render_controller.render_players([player])

    def show_filtered_players(self, **kwargs: Any) -> None:
        players = self.repository.get_players()
        filtered_players: list[Player] = []

        if not kwargs:
            return

        field_name, field_value = next(iter(kwargs.items()))

        for player in players:
            player_attr: str = str(getattr(player, field_name)).lower()
            if player_attr == field_value:
                filtered_players.append(player)

        self.render_controller.render_players(filtered_players)


ACTION_ROUTING: ActionRouting = {
    PlayerShortcut.CREATE_PLAYER.value.shortcut: PlayerController.create_new_player,
    PlayerShortcut.PLAYERS.value.shortcut: PlayerController.show_players,
    PlayerShortcut.SELECT_PLAYER.value.shortcut: PlayerController.show_player,
    PlayerShortcut.FILTER_PLAYER.value.shortcut: PlayerController.show_filtered_players,
    PlayerShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
