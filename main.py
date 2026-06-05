from rich.console import Console

from controllers.factories.player_action_runner import build_player_action_runner
from controllers.factories.tournament_action_runner import (
    build_tournament_action_runner,
)
from controllers.factories.main_action_runner import build_main_action_runner

from controllers.application_router import APPLICATION_ROUTER
from controllers.shortcuts.main import MainShortcut

ROOT = "ROOT"


def main():
    console = Console()
    main_runner = build_main_action_runner(console=console)
    player_runner = build_player_action_runner(console=console)
    tournament_runner = build_tournament_action_runner(console=console)

    APPLICATION_ROUTER.register(ROOT, main_runner)
    APPLICATION_ROUTER.register(
        MainShortcut.HANDLE_PLAYERS.value.shortcut, player_runner
    )
    APPLICATION_ROUTER.register(
        MainShortcut.HANDLE_TOURNAMENTS.value.shortcut, tournament_runner
    )

    APPLICATION_ROUTER.redirect_to(ROOT)


if __name__ == "__main__":
    main()
