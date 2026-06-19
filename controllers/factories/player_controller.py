from rich.console import Console

from core.core_view import CoreView, ListView
from view.player import PlayerView

from controllers.handlers.player import PlayerPromptHandler, PlayerRenderHandler
from controllers.player import PlayerController


def build_player_controller(
    console: Console,
    list_view: ListView,
) -> PlayerController:
    view = PlayerView(console=console)
    prompt_handler = PlayerPromptHandler(view=view)
    renderer_handler = PlayerRenderHandler(view=view)
    player_controller = PlayerController(
        prompt_handler=prompt_handler,
        renderer_handler=renderer_handler,
    )

    return player_controller
