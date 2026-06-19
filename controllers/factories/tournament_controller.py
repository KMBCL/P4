from rich.console import Console

from core.core_view import CoreView, ListView
from view.tournament import TournamentView


from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)
from controllers.tournament import TournamentController, TournamentSelector
from service.tournament import TournamentService


def build_tournament_controller(
    console: Console,
    list_view: ListView,
) -> TournamentController:
    view = TournamentView(console=console)
    prompt_handler = TournamentPromptHandler(view=view)
    renderer_handler = TournamentRenderHandler(view=view)
    service = TournamentService()
    selector = TournamentSelector(prompt_handler, renderer_handler, service)
    tournament_controller = TournamentController(
        prompt_handler=prompt_handler,
        renderer_handler=renderer_handler,
        service=service,
        selector=selector,
    )
    return tournament_controller
