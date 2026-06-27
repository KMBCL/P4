from view.build import console, list_view, tournament_view, player_view

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from controllers.handlers.player import (
    PlayerPromptHandler,
    PlayerRenderHandler,
)

tournament_prompt_handler = TournamentPromptHandler(tournament_view)
tournament_rendered_handler = TournamentRenderHandler(tournament_view)

player_prompt_handler = PlayerPromptHandler(player_view)
player_render_handler = PlayerRenderHandler(player_view)
