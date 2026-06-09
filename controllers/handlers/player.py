from core.core_handler import CorePromptHandler

from view.player import PlayerView

from controllers.validators.chess_id import ChessIDValidator


from core.core_renderer import CoreRenderer
from controllers.handlers.date import DatePromptHandler


from models.player import Player, PlayerInputData


class PlayerPromptHandler(CorePromptHandler):

    def __init__(self, view: PlayerView) -> None:
        self.view = view
        self.chess_id_validator = ChessIDValidator()
        self.date_prompt_handler = DatePromptHandler[Player](self.view)

    def get_player_input(self) -> PlayerInputData:
        return PlayerInputData(
            chess_id=self.prompt_chess_id(),
            last_name=self.prompt_last_name(),
            first_name=self.prompt_first_name(),
            birthdate=self.prompt_birthdate(),
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


class PlayerRenderHandler(CoreRenderer):

    def __init__(self, view: PlayerView) -> None:
        self.view = view

    def render_players(self, players: list[Player]):
        self.view.render_models(players)
