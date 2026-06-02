from __future__ import annotations

from views.player import PlayerView

from controllers.validators.chess_id import ChessIDValidator

from controllers.shortcuts.player import PlayerShortcuts

from controllers.handlers.date_prompt import DatePromptHandler
from controllers.handlers.action_prompt import ActionPromptHandler

from models.player import Player, PlayerInputData
from repository.player import PlayerRepository


class PlayerPromptHandler:

    def __init__(self, view: PlayerView) -> None:
        self.view = view
        self.chess_id_validator = ChessIDValidator()

        self.date_prompt_handler = DatePromptHandler[Player](self.view)
        self.action_prompt_handler = ActionPromptHandler[Player](self.view)

    def prompt_action(self) -> str:
        return self.action_prompt_handler.prompt_action(
            action_shortcuts=PlayerShortcuts
        )

    def prompt_chess_id(self) -> str:
        while True:
            user_input = self.view.prompt_chess_id()

            user_input_result = self.chess_id_validator.validate_chess_id(user_input)
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.required_reason)
                continue

            return user_input

    def prompt_last_name(self) -> str:
        return self.view.prompt_last_name()

    def prompt_first_name(self) -> str:
        return self.view.prompt_first_name()

    def prompt_birthdate(self) -> str:
        return self.date_prompt_handler.prompt_date(self.view.prompt_birthdate)


class PlayerRenderController:

    def __init__(self, view: PlayerView) -> None:
        self.view = view

    def render_players(self, players: list[Player]):
        self.view.render_models(players)


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

    def create_new_player(self) -> str:
        player = self.build_new_player(
            player_input=self.get_player_input(),
            new_pk=self.repository.make_new_pk(),
        )
        self.repository.write_data(json_data=player.to_json())
        return "success!"

    def show_players(self):
        players = self.repository.get_players()
        self.render_controller.render_players(players)

    def run(self):
        running = True
        while running:
            action = self.prompt_controller.prompt_action()
            if action == PlayerShortcuts.CREATE_PLAYER:
                self.create_new_player()
                continue

            if action == PlayerShortcuts.PLAYERS:
                self.show_players()
                continue
