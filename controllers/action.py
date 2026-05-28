from dataclasses import dataclass

from models.player import Player
from views.player_display import PlayerDisplay

from rich.console import Console


@dataclass
class Result:
    pass


class Action:
    action: str = "Kawabounga"

    def __init__(self, console: Console) -> None:
        self.console = console

    def run(self) -> None:
        print(f"{self.action} - DONE !!")


class CreatePlayer(Action):

    def create_player(self) -> Player:
        player_display = PlayerDisplay(console=self.console)
        player_data_input = player_display.display_create_player()
        new_player = Player(
            pk=1,
            chess_id=player_data_input.chess_id,
            last_name=player_data_input.last_name,
            first_name=player_data_input.first_name,
        )

        return new_player

    def run(self) -> None:
        self.create_player()
