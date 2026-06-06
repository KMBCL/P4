from rich.console import Console


from view.tournament import TournamentView
from repository.tournament import TournamentRepository

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)
from controllers.tournament import TournamentController


from controllers.shortcuts.tournament import TournamentShortcut
from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.menu_state import MenuState


from repository.tournament import TournamentRepository

ACTION_ROUTING: ActionRouting = {
    TournamentShortcut.CREATE_TOURNAMENT.value.shortcut: TournamentController.create_new_tournament,
    TournamentShortcut.TOURNAMENTS.value.shortcut: TournamentController.show_tournaments,
    TournamentShortcut.FILTER_TOURNAMENTS.value.shortcut: TournamentController.show_filtered_tournaments,
    TournamentShortcut.TOURNAMENT_ROUNDS.value.shortcut: TournamentController.show_tournament_rounds,
    TournamentShortcut.REGISTERED_PLAYERS.value.shortcut: TournamentController.show_tournament_players,
    TournamentShortcut.REGISTER_PLAYER.value.shortcut: TournamentController.register_player,
    TournamentShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}


def build_tournament_controller(console: Console) -> TournamentController:
    view = TournamentView(console=console)
    repository = TournamentRepository()
    prompt_handler = TournamentPromptHandler(view=view)
    renderer_handler = TournamentRenderHandler(view=view)
    tournament_controller = TournamentController(
        repository=repository,
        prompt_handler=prompt_handler,
        renderer_handler=renderer_handler,
    )
    return tournament_controller


def build_tournament_action_runner(console: Console) -> ActionRunner:
    tournament_controller = build_tournament_controller(console=console)
    action_runner = ActionRunner(
        target_controller=tournament_controller, action_routing=ACTION_ROUTING
    )

    return action_runner
