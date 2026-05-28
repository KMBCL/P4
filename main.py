from __future__ import annotations

from config.view_definitions import build_main_view
from controllers.view_controller import ViewControler
from controllers.view_renderer import ViewRenderer

from rich.console import Console


def main():
    console = Console()
    main_view = build_main_view()
    view_renderer = ViewRenderer(console=console)
    view_controller = ViewControler(root_view=main_view, view_renderer=view_renderer)
    view_controller.run_view()


if __name__ == "__main__":
    main()
