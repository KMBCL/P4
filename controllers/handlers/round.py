"""Prompts and renders the rounds."""

from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler


from view.round import RoundView


class RoundPromptHandler(CorePromptHandler[RoundView]):
    """Provides core prompting methods to class, awaiting for further feature."""

    pass


class RoundRenderHandler(CoreRenderer):
    """Holds the view of a round, and prints nothing of its own."""

    def __init__(self, view: RoundView) -> None:
        """Holds the view the handler prints through.

        Args:
            view (RoundView): The view to print through.
        """
        self.view = view
