from models.menu import MenuItem


class ShouldContinueToMenuItem:

    @staticmethod
    def should_continue_to_menu_item() -> list[MenuItem]:
        menu_items: list[MenuItem] = [
            MenuItem(code="yes", title="Yes", value=True),
            MenuItem(code="no", title="No", value=False),
        ]
        return menu_items
