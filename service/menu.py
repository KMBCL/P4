"""Reads the menu the user navigates."""

from repository.repository import Repository
from repository.paths import MENU_DIR
from models.menu import MenuStructure


class MenuService:
    """Reads the stored definition of the menu."""

    def __init__(self, repository: Repository) -> None:
        """Holds the repository the menu is read from.

        Args:
            repository (Repository): The repository to read through.
        """
        self.repository = repository

    def get_menu_structure(self) -> MenuStructure:
        """Reads the whole menu.

        Returns:
            MenuStructure: The menu, built from its stored definition.
        """
        return MenuStructure.from_json(self.repository.get_raw_models(MENU_DIR))
