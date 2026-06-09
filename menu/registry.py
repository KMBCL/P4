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


console = Console()
player_controller = build_player_controller(console)
tournament_controller = build_tournament_controller(console)


REGISTRY: ActionRouting = {
    PlayerMenuCode.CREATE_NEW_PLAYER: player_controller.create_new_player,
    PlayerMenuCode.SHOW_PLAYERS: player_controller.show_players,
    TournamentMenuCode.CREATE_NEW_TOURNAMENT: tournament_controller.create_new_tournament,
}
