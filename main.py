from __future__ import annotations


from rich.console import Console

from controllers.renderer import Renderer
from controllers.view_controller import ViewController

from views.view_path import ViewPath
from views.registry_builder import build_view_registry


def main():
    console = Console()
    renderer = Renderer(console)
    view_registry = build_view_registry()

    main_view = view_registry.get_required_view(ViewPath.MAIN_VIEW)
    view_controller = ViewController(
        renderer=renderer,
        main_view=main_view,
        view_registry=view_registry,
    )
    view_controller.run()


if __name__ == "__main__":
    main()
