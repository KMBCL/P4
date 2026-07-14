"""Starts the application."""

from build_menu import menu_controller

ROOT = "ROOT"


def main():
    """Runs the menu, until the user leaves the application."""
    menu_controller.get_menu_input()


if __name__ == "__main__":
    main()
