from menu.constants import MenuCode

from models.menu import MenuItem
from models.tournament import Tournament


class ModelToMenuItem:

    @staticmethod
    def tournament_to_menu_item(tournaments: list[Tournament]) -> list[MenuItem]:
        menu_items: list[MenuItem] = [
            MenuItem(
                code=tournament.pk,
                title=tournament.name,
            )
            for tournament in tournaments
        ]
        return menu_items


class MenuFromModels:

    @staticmethod
    def _build_back_menu_item() -> MenuItem:
        back = MenuItem(code=MenuCode.BACK, title="Back")
        return back

    @staticmethod
    def build_tournament_menu_items(tournaments: list[Tournament]) -> list[MenuItem]:
        tournament_menu_items = ModelToMenuItem.tournament_to_menu_item(tournaments)
        tournament_menu_items.append(MenuFromModels._build_back_menu_item())

        return tournament_menu_items
