"""Provides the base every prompt handler is built on."""

from typing import Callable, Generic, Any, TypeVar


from core.core_view import CoreView
from core.result import Result

TView = TypeVar("TView", bound=CoreView[Any])


class CorePromptHandler(Generic[TView]):
    """Bases a prompt handler, asking again until the input is valid."""

    def __init__(self, view: TView) -> None:
        """Holds the view the handler prompts through.

        Args:
            view (TView): The view to prompt through.
        """
        self.view = view

    def prompt(
        self,
        prompt_function: Callable[[], str],
        validation_function: Callable[[str], Result],
    ):
        """Asks the user until the input passes validation.

        The reason of a rejected input is rendered, then the user is asked again.

        Args:
            prompt_function (Callable[[], str]): The prompt to ask through.
            validation_function (Callable[[str], Result]): The validation to pass.

        Returns:
            str: The raw input, once validated.
        """
        while True:
            user_input = prompt_function()

            user_input_result = validation_function(user_input)
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.get_reason())
                continue

            return user_input
