"""Validates the choice made by the user in front of a menu."""

from core.result import Result
from models.menu import MenuItem


class MenuValidator:
    """Checks that a menu choice is a number designating a displayed item."""

    @staticmethod
    def validate_menu_choice(menu_input: str) -> Result:
        """Validates that the choice is a whole number.

        Args:
            menu_input (str): The raw choice typed by the user.

        Returns:
            Result:
                - A valid result carrying the parsed ``int``.
                - An invalid one when the input is not a number.
        """
        try:
            menu_number = int(menu_input)
            return Result.valid(value=menu_number)
        except ValueError:
            return Result.invalid("Invalid choice. Expected a number.")

    @staticmethod
    def is_choice_in_range(
        menu_input: str,
        available_items: list[MenuItem],
    ) -> Result:
        """Validate that choice is one of the displayed items.

        Args:
            menu_input (str): The raw choice typed by the user.
            available_items (list[MenuItem]): The items currently displayed, whose
                length gives the upper bound of the accepted range.

        Returns:
            Result:
                - A valid result carrying the chosen number.
                - An invalid one when the choice is not a number, or falls
                  outside the range.
        """
        MIN_RANGE = 1
        max_range = len(available_items)

        menu_number_result = MenuValidator.validate_menu_choice(menu_input)
        if not menu_number_result:
            return menu_number_result

        menu_number: int = menu_number_result.get_value()

        if not MIN_RANGE <= menu_number <= max_range:
            return Result.invalid(
                f"Choice expected between {MIN_RANGE} and {len(available_items)}"
            )

        return Result.valid(value=menu_number)
