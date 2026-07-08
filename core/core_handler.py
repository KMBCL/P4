from typing import Callable, Generic, Any, TypeVar


from core.core_view import CoreView
from core.result import Result

TView = TypeVar("TView", bound=CoreView[Any])


class CorePromptHandler(Generic[TView]):

    def __init__(self, view: TView) -> None:
        self.view = view

    def prompt(
        self,
        prompt_function: Callable[[], str],
        validation_function: Callable[[str], Result],
    ):

        while True:
            user_input = prompt_function()

            user_input_result = validation_function(user_input)
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.get_reason())
                continue

            return user_input
