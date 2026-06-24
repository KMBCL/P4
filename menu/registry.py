from __future__ import annotations

from enum import StrEnum
from typing import TypeAlias, Callable

from rich.console import Console
from core.core_view import ListView
from controllers.factories.menu_controller import build_menu_controller
from controllers.factories.player_controller import build_player_controller


from view.tournament import TournamentView
from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)
from controllers.tournament import (
    TournamentController,
    TournamentSelector,
    TournamentRunner,
    TournamentRounds,
    TournamentPlayer,
)
from service.tournament import TournamentService
from service.player import PlayerService

from controllers.menu_state import MenuState

Action: TypeAlias = Callable[..., MenuState | None]
ActionRouting: TypeAlias = dict[str, Action]


class PlayerMenuCode(StrEnum):
    CREATE_NEW_PLAYER = "create_new_player"
    SHOW_PLAYERS = "show_players"


class TournamentMenuCode(StrEnum):
    CREATE_NEW_TOURNAMENT = "create_new_tournament"
    SHOW_TOURNAMENTS = "show_tournaments"
    # SHOW_FILTERED_TOURNAMENTS = "show_filtered_tournaments"
    HANDLE_TOURNAMENT = "handle_tournament"
    CHANGE_TOURNAMENT = "change_tournament"
    SHOW_TOURNAMENT_ROUNDS = "show_tournament_rounds"
    SHOW_REGISTERED_PLAYERS = "show_register_players"
    REGISTER_PLAYER = "register_player"
    SET_ROUND_MATCHES = "set_round_matches"
    SET_MATCHES_SCORE = "set_matches_scores"
    RUN_TOURNAMENT = "run_tournament"


console = Console()
list_view = ListView(console)


player_controller = build_player_controller(console, list_view)

player_service = PlayerService()

tournament_view = TournamentView(console)
tournament_prompt_handler = TournamentPromptHandler(tournament_view)
tournament_rendered_handler = TournamentRenderHandler(tournament_view)
tournament_service = TournamentService()
tournament_selector = TournamentSelector(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
)
tournament_controller = TournamentController(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
)
tournament_runner = TournamentRunner(
    tournament_prompt_handler,
    tournament_rendered_handler,
    tournament_service,
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

REGISTRY: ActionRouting = {
    PlayerMenuCode.CREATE_NEW_PLAYER: player_controller.create_new_player,
    PlayerMenuCode.SHOW_PLAYERS: player_controller.show_players,
    TournamentMenuCode.CREATE_NEW_TOURNAMENT: tournament_controller.create_new_tournament,
    TournamentMenuCode.SHOW_TOURNAMENTS: tournament_controller.show_tournaments,
    TournamentMenuCode.HANDLE_TOURNAMENT: tournament_selector.handle_tournament,
    TournamentMenuCode.CHANGE_TOURNAMENT: tournament_selector.change_tournament,
    TournamentMenuCode.SHOW_TOURNAMENT_ROUNDS: tournament_rounds.show_tournament_rounds,
    TournamentMenuCode.SHOW_REGISTERED_PLAYERS: tournament_player.show_register_players,
    TournamentMenuCode.REGISTER_PLAYER: tournament_player.register_player,
    TournamentMenuCode.RUN_TOURNAMENT: tournament_runner.run_tournament,
}

menu_controller = build_menu_controller(console, list_view, REGISTRY)
