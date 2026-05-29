from __future__ import annotations


from rich.console import Console

from controllers.renderer import Renderer
from controllers.view_controller import ViewController


def main():
    console = Console()
    renderer = Renderer(console)
    view_controller = ViewController(renderer)
    view_controller.run()


if __name__ == "__main__":
    main()
