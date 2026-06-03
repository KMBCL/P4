from __future__ import annotations

from views.player import PlayerView

from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.shortcuts.player import PlayerShortcut
from controllers.handlers.player import PlayerPromptHandler, PlayerRenderController
from controllers.menu_state import MenuState

from models.player import Player, PlayerInputData
from repository.player import PlayerRepository


class PlayerController:

    def __init__(self, view: PlayerView) -> None:
        self.repository = PlayerRepository()
        self.prompt_handler = PlayerPromptHandler(view=view)
        self.render_controller = PlayerRenderController(view=view)

        self.action_runner = ActionRunner(
            target_controller=self,
            action_routing=ACTION_ROUTING,
            prompt_handler=self.prompt_handler,
            render_controller=self.render_controller,
        )

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

    def run(self):
        self.action_runner.run()


ACTION_ROUTING: ActionRouting = {
    PlayerShortcut.CREATE_PLAYER.value.shortcut: PlayerController.create_new_player,
    PlayerShortcut.PLAYERS.value.shortcut: PlayerController.show_players,
    PlayerShortcut.BACK.value.shortcut: lambda _: MenuState.break_loop(),
}
