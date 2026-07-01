from repository.repository import Repository
from repository.paths import MENU_DIR
from models.menu import MenuStructure


class MenuService:

    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def get_menu_structure(self) -> MenuStructure:
        return MenuStructure.from_json(self.repository.get_raw_models(MENU_DIR))
