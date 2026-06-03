from rich.console import Console

from controllers.main import MainController


def main():
    console = Console()
    main_controller = MainController(console=console)
    main_controller.run()


if __name__ == "__main__":
    main()
