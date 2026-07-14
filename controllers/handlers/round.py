"""Prompts and renders the rounds."""

from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler


from view.round import RoundView


class RoundPromptHandler(CorePromptHandler[RoundView]):
    """Asks the user for the timestamps of a round."""

    def prompt_start_datetime(self) -> str:
        """Asks when the round started.

        Returns:
            str: The raw timestamp, unvalidated.
        """
        return self.view.prompt_start_datetime()

    def prompt_end_timestamp(self) -> str:
        """Asks when the round ended.

        Returns:
            str: The raw timestamp, unvalidated.
        """
        return self.view.prompt_end_timestamp()


class RoundRenderHandler(CoreRenderer):
    """Holds the view of a round, and prints nothing of its own."""

    def __init__(self, view: RoundView) -> None:
        """Holds the view the handler prints through.

        Args:
            view (RoundView): The view to print through.
        """
        self.view = view
