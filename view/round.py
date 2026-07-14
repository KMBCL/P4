"""Prompts the user for the timestamps of a round."""

from core.core_view import CoreView
from models.round import Round


class RoundView(CoreView[Round]):
    """Asks the user when a round started and when it ended."""

    def prompt_start_datetime(self):
        """Asks when the round started.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("Start datetime - YYYY-MM-DD HH:MM")

    def prompt_end_timestamp(self):
        """Asks when the round ended.

        Returns:
            str: The raw input, unvalidated.
        """
        return self.prompt("End datetime - YYYY-MM-DD HH:MM")
