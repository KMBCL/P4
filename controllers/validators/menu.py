from controllers.result import Result
from models.menu import MenuItem


class MenuValidator:

    def make_available_item_expected_message(self, choice_codes: list[str]) -> str:
        separator = ", "
        return separator.join(choice_codes)

    def validate_menu_choice(
        self, menu_input: str, available_items: list[MenuItem]
    ) -> Result:
        try:
            menu_item_number = int(menu_input)
        except:
            return Result.invalid(f"Invalid choice")

        if menu_item_number > len(available_items):
            return Result.invalid(f"Invalid choice")

        return Result.valid()
