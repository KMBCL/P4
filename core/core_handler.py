from typing import Any
from enum import Enum

from controllers.handlers.action import ActionPromptHandler


class CorePromptHandler:

    def __init__(
        self,
        action_prompt_handler: ActionPromptHandler[Any],
        action_shortcuts: type[Enum],
    ) -> None:
        self.action_prompt_handler = action_prompt_handler
        self.action_shortcuts = action_shortcuts

    def prompt_action(self) -> tuple[str, dict[str, str]]:
        return self.action_prompt_handler.prompt_action(
            action_shortcuts=self.action_shortcuts
        )
