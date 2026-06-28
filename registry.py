from __future__ import annotations

from enum import StrEnum
from typing import TypeAlias, Callable


from controllers.menu_state import MenuState

import controllers.build as Controllers

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


REGISTRY: ActionRouting = {
    PlayerMenuCode.CREATE_NEW_PLAYER: Controllers.player_controller.create_new_player,
    PlayerMenuCode.SHOW_PLAYERS: Controllers.player_controller.show_players,
    TournamentMenuCode.CREATE_NEW_TOURNAMENT: Controllers.tournament_controller.create_new_tournament,
    TournamentMenuCode.SHOW_TOURNAMENTS: Controllers.tournament_controller.show_tournaments,
    TournamentMenuCode.HANDLE_TOURNAMENT: Controllers.tournament_selector.handle_tournament,
    TournamentMenuCode.CHANGE_TOURNAMENT: Controllers.tournament_selector.change_tournament,
    # TournamentMenuCode.SHOW_TOURNAMENT_ROUNDS: Controllers.tournament_rounds.show_tournament_rounds,
    TournamentMenuCode.SHOW_REGISTERED_PLAYERS: Controllers.tournament_player.show_register_players,
    TournamentMenuCode.REGISTER_PLAYER: Controllers.tournament_player.register_player,
    TournamentMenuCode.RUN_TOURNAMENT: Controllers.tournament_runner.run_tournament,
}
