from __future__ import annotations


from rich.console import Console


from views.player import PlayerView
from controllers.player import PlayerController
from controllers.tournament import TournamentController


def main():
    console = Console()
    player_display = PlayerView(console=console)
    player_controller = PlayerController(view=player_display)
    player_controller.run()


if __name__ == "__main__":
    main()
