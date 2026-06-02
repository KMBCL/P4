from enum import StrEnum

from controllers.result import Result


class ActionValidator:

    def validate_action_input(
        self, user_input: str, action_shortcuts: type[StrEnum]
    ) -> Result:
        return (
            Result.valid()
            if user_input in action_shortcuts
            else Result.invalid(
                reason=f"{user_input} is not valid! Please select available shortcut"
            )
        )
