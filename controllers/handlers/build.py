"""Builds the handlers, one prompt and one render handler per view."""

from view.build import (
    core_view,
    tournament_view,
    player_view,
    round_view,
)

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from controllers.handlers.player import (
    PlayerPromptHandler,
    PlayerRenderHandler,
)

from controllers.handlers.round import (
    RoundPromptHandler,
    RoundRenderHandler,
)

from controllers.handlers.menu import (
    MenuPromptHandler,
    MenuRendererHandler,
)

tournament_prompt_handler = TournamentPromptHandler(tournament_view)
tournament_rendered_handler = TournamentRenderHandler(tournament_view)

player_prompt_handler = PlayerPromptHandler(player_view)
player_render_handler = PlayerRenderHandler(player_view)

round_prompt_handler = RoundPromptHandler(round_view)
round_render_handler = RoundRenderHandler(round_view)

menu_prompt_handler = MenuPromptHandler(core_view)
menu_render_handler = MenuRendererHandler(core_view)
