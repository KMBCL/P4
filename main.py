from __future__ import annotations

from config.menu_definitions import build_root_menu
from views.menu_display import MenuDisplay
from controllers.menu_runner import MenuRunner


def main():
    menu_display = MenuDisplay()
    menu_renderer = MenuRunner(
        root_item=build_root_menu(),
        menu_display=menu_display,
    )
    menu_renderer.run_menu()


if __name__ == "__main__":
    main()
