from typing import Any

from rich.console import Console

from controllers.action_routing import ActionRouting

from controllers.shortcuts.playertournament import PlayerTournamentShortcut

from controllers.menu_state import MenuState


class PlayerTournamentController:

    def __init__(self):
        pass

    def add_player_to_tournament(self, kwargs: Any) -> None:
        pass


ACTION_ROUTING: ActionRouting = {
    PlayerTournamentShortcut.ADD_PLAYER_TO_TOURNAMENT.value.shortcut: PlayerTournamentController.add_player_to_tournament,
    PlayerTournamentShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}
