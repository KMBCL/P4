"""Prompts the user for the fields of a tournament."""

from core.core_view import CoreView

from models.tournament import Tournament


class TournamentView(CoreView[Tournament]):
    """Asks the user for each field of a tournament, one at a time."""

    def prompt_name(self) -> str:
        """Asks for the name of the tournament.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Name")

    def prompt_place(self) -> str:
        """Asks for the place of the tournament.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Place")

    def prompt_start_date(self) -> str:
        """Asks for the start date of the tournament.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Start date - YYYY-MM-DD")

    def prompt_end_date(self) -> str:
        """Asks for the end date of the tournament.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("End date - YYYY-MM-DD")

    def prompt_description(self) -> str:
        """Asks for the description of the tournament.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Description")

    def prompt_round_count(self) -> str:
        """Asks for the number of rounds the tournament will run.

        Returns:
            str: The raw input, unvalidated. An empty input keeps the default.
        """
        return self.prompt("Round count - default=4")

    def prompt_register_player(self) -> str:
        """Asks for the last name of the player to register.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Register player by last name")

    def render_setting_scores_for_round(self, round_name: str) -> None:
        """Announces the round whose scores are about to be entered.

        Args:
            round_name (str): The name of the round.
        """
        return self.console.print(f"Setting scores for {round_name}")
