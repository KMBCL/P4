from menu.menu import MenuService

ROOT = "ROOT"


def main():
    menu_service = MenuService()
    menu_service.get_menu_input()


if __name__ == "__main__":
    main()
