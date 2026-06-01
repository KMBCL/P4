from __future__ import annotations


from rich.console import Console

from controllers.renderer import Renderer
from controllers.view_controller import ViewController

from views.view_path import ViewPath
from views.registry import VIEW_REGISTRY
import views.build_views


def main():
    console = Console()
    renderer = Renderer(console)
    main_view = VIEW_REGISTRY.get_required_view(ViewPath.MAIN_VIEW)
    view_controller = ViewController(
        renderer=renderer,
        main_view=main_view,
    )
    view_controller.run()


if __name__ == "__main__":
    main()
