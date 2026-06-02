from views.player import PlayerView

from controllers.shortcuts.player import PlayerShortcut

from controllers.handlers.player import PlayerPromptHandler, PlayerRenderController

from models.player import Player, PlayerInputData
from repository.player import PlayerRepository


class PlayerController:

    def __init__(self, view: PlayerView) -> None:
        self.repository = PlayerRepository()
        self.prompt_controller = PlayerPromptHandler(view=view)
        self.render_controller = PlayerRenderController(view=view)

    def build_new_player(self, player_input: PlayerInputData, new_pk: int):
        new_player = Player.from_player_input(new_pk=new_pk, player_input=player_input)
        return new_player

    def get_player_input(self) -> PlayerInputData:
        return PlayerInputData(
            chess_id=self.prompt_controller.prompt_chess_id(),
            last_name=self.prompt_controller.prompt_last_name(),
            first_name=self.prompt_controller.prompt_first_name(),
            birthdate=self.prompt_controller.prompt_birthdate(),
        )

    def create_new_player(self):
        player = self.build_new_player(
            player_input=self.get_player_input(),
            new_pk=self.repository.make_new_pk(),
        )
        self.repository.write_data(json_data=player.to_json())

    def show_players(self):
        players = self.repository.get_players()
        self.render_controller.render_players(players)

    def run(self):
        running = True
        while running:
            action = self.prompt_controller.prompt_action()
            if action == PlayerShortcut.CREATE_PLAYER:
                self.create_new_player()
                continue

            if action == PlayerShortcut.PLAYERS:
                self.show_players()
                continue
