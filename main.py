from view.build import console, list_view
from controllers.factories.menu_structure import build_menu_structure

from controllers.factories.menu_controller import build_menu_controller

from registry import REGISTRY

ROOT = "ROOT"


def main():
    menu_structure = build_menu_structure()
    menu_controller = build_menu_controller(
        console, list_view, REGISTRY, menu_structure
    )
    menu_controller.get_menu_input()


if __name__ == "__main__":
    main()
