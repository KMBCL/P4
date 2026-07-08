from core.core_view import CoreView
from models.player import Player


class PlayerView(CoreView[Player]):

    def prompt_chess_id(self) -> str:
        return self.prompt("Chess id - Ex: AB13579")

    def prompt_last_name(self) -> str:
        return self.prompt("Last name")

    def prompt_first_name(self) -> str:
        return self.prompt("First name")

    def prompt_birthdate(self) -> str:
        return self.prompt("Birthdate - YYYY-MM-DD")
