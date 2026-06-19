from core.core_handler import CorePromptHandler

from view.player import PlayerView

from controllers.validators.chess_id import ChessIDValidator
from controllers.validators.date import DateValidator

from core.core_renderer import CoreRenderer


from models.player import Player, PlayerInputData


class PlayerPromptHandler(CorePromptHandler[PlayerView]):

    def __init__(self, view: PlayerView) -> None:
        self.view = view

    def get_player_input(self) -> PlayerInputData:
        return PlayerInputData(
            chess_id=self.prompt_chess_id(),
            last_name=self.prompt_last_name(),
            first_name=self.prompt_first_name(),
            birthdate=self.prompt_birthdate(),
        )

    def prompt_chess_id(self) -> str:
        return self.prompt(
            self.view.prompt_chess_id, ChessIDValidator.validate_chess_id
        )

    def prompt_last_name(self) -> str:
        return self.view.prompt_last_name()

    def prompt_first_name(self) -> str:
        return self.view.prompt_first_name()

    def prompt_birthdate(self) -> str:
        return self.prompt(self.view.prompt_birthdate, DateValidator.validate_date)


class PlayerRenderHandler(CoreRenderer):

    def __init__(self, view: PlayerView) -> None:
        self.view = view

    def render_players(self, players: list[Player]):
        self.view.console.print("*** Player list ***")

        for player in players:
            self.view.console.print(
                f"Chess id : '{player.chess_id}' - '{player.last_name} {player.first_name}' - Birthdate : '{player.birthdate}'"
            )
