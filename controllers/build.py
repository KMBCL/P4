from service.build import (
    tournament_service,
    tournament_standing_service,
    player_service,
    round_service,
)
from controllers.handlers.build import (
    tournament_prompt_handler,
    tournament_rendered_handler,
    player_prompt_handler,
    player_render_handler,
    round_prompt_handler,
    round_render_handler,
)

from controllers.tournament import (
    TournamentController,
    TournamentSelector,
    TournamentRunner,
    TournamentPlayer,
)
from controllers.round import RoundController
from controllers.player import PlayerController

round_controller = RoundController(
    round_prompt_handler,
    round_render_handler,
    round_service,
    tournament_service,
    tournament_standing_service,
)


tournament_selector = TournamentSelector(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
)

tournament_runner = TournamentRunner(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
    round_controller,
)

tournament_player = TournamentPlayer(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
    player_service,
    player_render_handler,
)

tournament_controller = TournamentController(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
    tournament_standing_service,
)

player_controller = PlayerController(
    player_prompt_handler,
    player_render_handler,
    player_service,
)
