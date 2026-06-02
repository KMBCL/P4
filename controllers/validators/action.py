from enum import Enum

from controllers.shortcuts.core_shortcuts import ShortcutDefinition
from controllers.result import Result


class ActionValidator:

    def validate_action_input(
        self, user_input: str, action_shortcuts: type[Enum]
    ) -> Result:
        cleaned_user_input = user_input.upper()

        for member in action_shortcuts:
            shortcut_definition: ShortcutDefinition = member.value

            if shortcut_definition.shortcut.upper() == cleaned_user_input:
                return Result.valid()

        return Result.invalid(
            reason=f"{user_input} is not valid! Please select available shortcut"
        )
