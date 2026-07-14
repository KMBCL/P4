"""Prompts the user for the fields of a player."""

from core.core_view import CoreView
from models.player import Player


class PlayerView(CoreView[Player]):
    """Asks the user for each field of a player, one at a time."""

    def prompt_chess_id(self) -> str:
        """Asks for the chess id of the player.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Chess id - Ex: AB13579")

    def prompt_last_name(self) -> str:
        """Asks for the last name of the player.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Last name")

    def prompt_first_name(self) -> str:
        """Asks for the first name of the player.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("First name")

    def prompt_birthdate(self) -> str:
        """Asks for the birthdate of the player.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Birthdate - YYYY-MM-DD")
