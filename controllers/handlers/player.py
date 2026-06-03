from views.player import PlayerView

from controllers.validators.chess_id import ChessIDValidator

from controllers.shortcuts.player import PlayerShortcut

from core.core_handler import PromptHandler
from controllers.handlers.date_prompt import DatePromptHandler
from controllers.handlers.action_prompt import ActionPromptHandler

from models.player import Player


class PlayerPromptHandler(PromptHandler):

    def __init__(self, view: PlayerView) -> None:
        self.view = view
        self.chess_id_validator = ChessIDValidator()

        self.date_prompt_handler = DatePromptHandler[Player](self.view)
        self.action_prompt_handler = ActionPromptHandler[Player](self.view)

    def prompt_action(self) -> tuple[str, dict[str, str]]:
        return self.action_prompt_handler.prompt_action(action_shortcuts=PlayerShortcut)

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

    def render_undefined_action(self, action: str):
        self.view.render_invalid_input(
            reason=f"{action} shortcut exists, but no action handled"
        )
