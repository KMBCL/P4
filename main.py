from __future__ import annotations


from rich.console import Console


from views.player import PlayerDisplay


def main():
    console = Console()
    player_display = PlayerDisplay(console=console)
    player_display.input_action()


if __name__ == "__main__":
    main()
