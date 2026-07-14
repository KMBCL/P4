"""Builds the handlers, one prompt and one render handler per view."""

from view.build import (
    core_view,
    tournament_view,
    player_view,
    round_view,
)

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRendererHandler,
)

from controllers.handlers.player import (
    PlayerPromptHandler,
    PlayerRendererHandler,
)

from controllers.handlers.round import (
    RoundPromptHandler,
    RoundRendererHandler,
)

from controllers.handlers.menu import (
    MenuPromptHandler,
    MenuRendererHandler,
)

tournament_prompt_handler = TournamentPromptHandler(tournament_view)
tournament_renderer_handler = TournamentRendererHandler(tournament_view)

player_prompt_handler = PlayerPromptHandler(player_view)
player_renderer_handler = PlayerRendererHandler(player_view)

round_prompt_handler = RoundPromptHandler(round_view)
round_renderer_handler = RoundRendererHandler(round_view)

menu_prompt_handler = MenuPromptHandler(core_view)
menu_renderer_handler = MenuRendererHandler(core_view)
