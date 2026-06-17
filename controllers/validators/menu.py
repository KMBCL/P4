from core.result import Result
from models.menu import MenuItem


class MenuValidator:

    @staticmethod
    def validate_menu_choice(menu_input: str) -> Result:
        try:
            menu_number = int(menu_input)
            return Result.valid(value=menu_number)
        except:
            return Result.invalid(f"Invalid choice. Expected a number.")

    @staticmethod
    def is_choice_in_range(menu_input: str, available_items: list[MenuItem]) -> Result:
        MIN_RANGE = 1
        max_range = len(available_items)

        menu_number_result = MenuValidator.validate_menu_choice(menu_input)
        if not menu_number_result:
            return menu_number_result

        menu_number: int = menu_number_result.required_value

        if not MIN_RANGE <= menu_number <= max_range:
            return Result.invalid(
                f"Choice expected between {MIN_RANGE} and {len(available_items)}"
            )

        return Result.valid()
