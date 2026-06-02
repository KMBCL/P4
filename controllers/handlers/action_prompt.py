from __future__ import annotations

from typing import Callable, Generic
from enum import StrEnum

from controllers.validators.action import ActionValidator

from views.core_view import CoreView
from models.core_model import TModel


class ActionPromptHandler(Generic[TModel]):

    def __init__(self, view: CoreView[TModel]) -> None:
        self.view = view
        self.validator = ActionValidator()

    def prompt_action(self, action_shortcuts: type[StrEnum]) -> str:
        while True:
            self.view.render_available_actions()
            user_input = self.view.prompt_action()

            user_input_result = self.validator.validate_action_input(
                user_input,
                action_shortcuts=action_shortcuts,
            )
            if not user_input_result:
                self.view.render_invalid_input(
                    reason=user_input_result.required_reason,
                )
                continue

            return user_input
