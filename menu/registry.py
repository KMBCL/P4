from __future__ import annotations

from enum import StrEnum
from typing import TypeAlias, Callable, Any, Self
from dataclasses import dataclass, field

from rich.console import Console

from controllers.factories.player_action_runner import build_player_controller
from controllers.factories.tournament_action_runner import build_tournament_controller

from core.core_data_repository import CoreDataRepository, MENU_DIR
from core.core_model import Model

from controllers.menu_state import MenuState

Action: TypeAlias = Callable[..., MenuState | None]
ActionRouting: TypeAlias = dict[str, Action]


class MenuCode(StrEnum):
    EXIT = "exit"
    BACK = "back"


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


console = Console()
player_controller = build_player_controller(console)
tournament_controller = build_tournament_controller(console)


REGISTRY: ActionRouting = {
    PlayerMenuCode.CREATE_NEW_PLAYER: player_controller.create_new_player,
    PlayerMenuCode.SHOW_PLAYERS: player_controller.show_players,
    TournamentMenuCode.CREATE_NEW_TOURNAMENT: tournament_controller.create_new_tournament,
    TournamentMenuCode.SHOW_TOURNAMENTS: tournament_controller.show_tournaments,
    TournamentMenuCode.HANDLE_TOURNAMENT: tournament_controller.handle_tournament,
    TournamentMenuCode.CHANGE_TOURNAMENT: tournament_controller.change_tournament,
    TournamentMenuCode.SHOW_TOURNAMENT_ROUNDS: tournament_controller.show_tournament_rounds,
    TournamentMenuCode.SHOW_REGISTERED_PLAYERS: tournament_controller.show_register_players,
    TournamentMenuCode.REGISTER_PLAYER: tournament_controller.register_player,
    TournamentMenuCode.SET_ROUND_MATCHES: tournament_controller.set_round_matches,
    TournamentMenuCode.SET_MATCHES_SCORE: tournament_controller.set_matches_scores,
}
