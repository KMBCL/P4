from typing import Generic
from enum import Enum

from controllers.validators.action import ActionValidator

from core.core_view import CoreView
from models.core_model import TModel


class ActionPromptHandler(Generic[TModel]):

    def __init__(self, view: CoreView[TModel]) -> None:
        self.view = view
        self.validator = ActionValidator()

    def _parse_user_input(self, user_input: str) -> tuple[str, str]:
        KWARGS_SEPARATOR = ":"
        EMPTY_ARGS = ""
        if KWARGS_SEPARATOR not in user_input:
            return user_input, EMPTY_ARGS

        action_shortcut, raw_args = user_input.split(KWARGS_SEPARATOR, 1)
        return action_shortcut.upper(), raw_args.lower()

    def _parse_kwargs(self, raw_args: str) -> dict[str, str]:
        ARGS_SPLITTER = ","
        KEY_VALUE_SEPARATOR = "="
        kwargs: dict[str, str] = {}

        for pair in raw_args.split(ARGS_SPLITTER):
            if KEY_VALUE_SEPARATOR in pair:
                key, value = pair.split(KEY_VALUE_SEPARATOR, 1)
                kwargs[key.strip()] = value.strip()

        return kwargs

    def prompt_action(self, action_shortcuts: type[Enum]) -> tuple[str, dict[str, str]]:
        while True:
            self.view.render_available_actions(action_shortcuts)
            user_input = self.view.prompt_action()

            action_shortcut, raw_args = self._parse_user_input(user_input)
            kwargs = self._parse_kwargs(raw_args)

            user_input_result = self.validator.validate_action_input(
                user_input=action_shortcut,
                action_shortcuts=action_shortcuts,
            )
            if not user_input_result:
                self.view.render_invalid_input(
                    reason=user_input_result.required_reason,
                )
                continue

            return action_shortcut, kwargs
