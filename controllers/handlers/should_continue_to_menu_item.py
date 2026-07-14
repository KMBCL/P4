"""Builds the menu entries of a yes or no question."""

from models.menu import MenuItem


class ShouldContinueToMenuItem:
    """Turns a yes or no question into menu entries the user picks from."""

    @staticmethod
    def should_continue_to_menu_item() -> list[MenuItem]:
        """Builds the two entries of a yes or no question.

        Each entry carries the answer it stands for, as its value.

        Returns:
            list[MenuItem]: The entry carrying True, then the one carrying False.
        """
        menu_items: list[MenuItem] = [
            MenuItem(code="yes", title="Yes", value=True),
            MenuItem(code="no", title="No", value=False),
        ]
        return menu_items
