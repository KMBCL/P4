from core.core_view import CoreView

from models.tournament import Tournament


class TournamentView(CoreView[Tournament]):

    def prompt_name(self) -> str:
        return self.prompt("Name")

    def prompt_place(self) -> str:
        return self.prompt("Place")

    def prompt_start_date(self) -> str:
        return self.prompt("Start date - YYYY-MM-DD")

    def prompt_end_date(self) -> str:
        return self.prompt("End date - YYYY-MM-DD")

    def prompt_description(self) -> str:
        return self.prompt("Description")

    def prompt_round_count(self) -> str:
        return self.prompt("Round count - default=4")

    def prompt_register_player(self) -> str:
        return self.prompt("Register player by last name")

    def render_setting_scores_for_round(self, round_name: str) -> None:
        return self.console.print(f"Setting scores for {round_name}")
