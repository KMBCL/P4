"""Prompts and renders the players."""

from core.core_handler import CorePromptHandler
from core.color import ColorHelper, Formatter

from view.player import PlayerView

from controllers.validators.chess_id import ChessIDValidator
from controllers.validators.date import DateValidator

from core.core_renderer import CoreRenderer


from models.player import Player, PlayerInputData


class PlayerPromptHandler(CorePromptHandler[PlayerView]):
    """Asks the user for a player, validating the fields that have a format."""

    def __init__(self, view: PlayerView) -> None:
        """Holds the view the handler prompts through.

        Args:
            view (PlayerView): The view to prompt through.
        """
        self.view = view

    def get_player_input(self) -> PlayerInputData:
        """Asks the user for every field of a player.

        Returns:
            PlayerInputData: The raw fields, ready to be given to the service.
        """
        self.view.skip_line()
        return PlayerInputData(
            chess_id=self.prompt_chess_id(),
            last_name=self.prompt_last_name(),
            first_name=self.prompt_first_name(),
            birthdate=self.prompt_birthdate(),
        )

    def prompt_chess_id(self) -> str:
        """Asks for the chess id, until its format is the expected one.

        Returns:
            str: The raw chess id, once validated.
        """
        return self.prompt(
            self.view.prompt_chess_id, ChessIDValidator.validate_chess_id
        )

    def prompt_last_name(self) -> str:
        """Asks for the last name, which has no format to validate.

        Returns:
            str: The raw last name, unvalidated.
        """
        return self.view.prompt_last_name()

    def prompt_first_name(self) -> str:
        """Asks for the first name, which has no format to validate.

        Returns:
            str: The raw first name, unvalidated.
        """
        return self.view.prompt_first_name()

    def prompt_birthdate(self) -> str:
        """Asks for the birthdate, until its format is the expected one.

        Returns:
            str: The raw birthdate, once validated.
        """
        return self.prompt(self.view.prompt_birthdate, DateValidator.validate_date)


class PlayerRenderHandler(CoreRenderer):
    """Prints the players, one line each."""

    def __init__(self, view: PlayerView) -> None:
        """Holds the view the handler prints through.

        Args:
            view (PlayerView): The view to print through.
        """
        self.view = view

    def render_players(self, players: list[Player]):
        """Prints every player, with their birthdate and their chess id.

        Args:
            players (list[Player]): The players to print.
        """
        self.view.skip_line()
        self.view.console.print(ColorHelper.title("Players"))

        for player in players:
            player_diplayed_name = f"{player.last_name} {player.first_name}"
            player_display = (
                ColorHelper.value(player_diplayed_name)
                + Formatter.label_value("Birthdate", player.birthdate)
                + Formatter.label_value("Chess id", player.chess_id)
            )
            self.view.console.print(player_display)
        self.view.skip_line()
