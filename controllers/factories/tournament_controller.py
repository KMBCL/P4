from rich.console import Console


from view.tournament import TournamentView


from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)
from controllers.tournament import TournamentController


def build_tournament_controller(console: Console) -> TournamentController:
    view = TournamentView(console=console)
    prompt_handler = TournamentPromptHandler(view=view)
    renderer_handler = TournamentRenderHandler(view=view)
    tournament_controller = TournamentController(
        prompt_handler=prompt_handler,
        renderer_handler=renderer_handler,
    )
    return tournament_controller
