from core.core_view import CoreView
from models.player_registration import PlayerRegistration


class PlayerRegistrationView(CoreView[PlayerRegistration]):

    def prompt_player_pk(self) -> str:
        return self.console.input("Player pk")

    def prompt_tournament_pk(self) -> str:
        return self.console.input("Tournament pk")
