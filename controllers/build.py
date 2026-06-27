from service.build import tournament_service, player_service, round_service
from controllers.handlers.build import (
    tournament_prompt_handler,
    tournament_rendered_handler,
    player_prompt_handler,
    player_render_handler,
)

from controllers.tournament import (
    TournamentController,
    TournamentSelector,
    TournamentRunner,
    TournamentRounds,
    TournamentPlayer,
)

from controllers.player import PlayerController

tournament_selector = TournamentSelector(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
)

tournament_runner = TournamentRunner(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
    round_service,
)
tournament_rounds = TournamentRounds(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
)
tournament_player = TournamentPlayer(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
    player_service,
)

tournament_controller = TournamentController(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
)

player_controller = PlayerController(
    player_prompt_handler,
    player_render_handler,
)
