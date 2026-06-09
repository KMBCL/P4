from core.core_view import CoreView
from models.tournament import Tournament


class TournamentView(CoreView[Tournament]):

    def prompt_name(self) -> str:
        return self.console.input("Name : ")

    def prompt_place(self) -> str:
        return self.console.input("Place : ")

    def prompt_start_date(self) -> str:
        return self.console.input("Start date - 'YYYY-MM-DD' : ")

    def prompt_end_date(self) -> str:
        return self.console.input("End date - 'YYYY-MM-DD' : ")

    def prompt_description(self) -> str:
        return self.console.input("Description : ")

    def prompt_round_count(self) -> str:
        return self.console.input("Round count - default=4 : ")

    def prompt_action(self) -> str:
        return self.console.input("Select choice : ").upper()

    def prompt_player_chess_id(self) -> str:
        return self.console.input("Player chess id : ")

    def prompt_tournament_pk(self) -> str:
        return self.console.input("Select tournament by 'pk' : ")

    def prompt_round_name(self) -> str:
        return self.console.input("Round name : ")
