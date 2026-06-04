from typing import Callable, Generic

from core.core_view import CoreView
from models.core_model import TModel

from controllers.validators.date import DateValidator


class DatePromptHandler(Generic[TModel]):

    def __init__(self, view: CoreView[TModel]) -> None:
        self.view = view
        self.validator = DateValidator()

    def prompt_date(self, view_prompt_method: Callable[[], str]) -> str:
        while True:
            user_input: str = view_prompt_method()

            user_input_result = self.validator.validate_date(user_input)
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.required_reason)
                continue

            return user_input
