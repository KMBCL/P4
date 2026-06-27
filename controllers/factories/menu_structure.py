from typing import Any


from core.core_data_repository import CoreDataRepository, MENU_DIR
from core.core_model import Model
from models.menu import MenuStructure


def build_menu_structure() -> MenuStructure:
    repository = CoreDataRepository[Any](Model)
    return MenuStructure.from_json(repository.read_json_file(MENU_DIR))
