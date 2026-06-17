from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler
from core.constants import WinningCondition


from view.tournament import TournamentView
from controllers.validators.chess_id import ChessIDValidator
from controllers.validators.date import DateValidator

from models.tournament import Tournament, TournamentInputData


class TournamentPromptHandler(CorePromptHandler[TournamentView]):

    def get_tournament_input(self):
        return TournamentInputData(
            name=self.prompt_name(),
            place=self.prompt_place(),
            start_date=self.prompt_start_date(),
            end_date=self.prompt_end_date(),
            description=self.prompt_description(),
            round_count=self.prompt_round_count(),
        )

    def get_player_registration_input(self):
        return self.prompt(
            self.view.prompt_register_player, ChessIDValidator.validate_chess_id
        )

    def get_tournament_pk_input(self) -> str:
        return self.prompt_tournament_pk()

    def get_round_name(self) -> str:
        return self.view.prompt_round_name()

    def prompt_name(self) -> str:
        return self.view.prompt_name()

    def prompt_place(self) -> str:
        return self.view.prompt_place()

    def prompt_description(self) -> str:
        return self.view.prompt_description()

    def prompt_round_count(self) -> str:
        return self.view.prompt_round_count()

    def prompt_start_date(self) -> str:
        return self.prompt(self.view.prompt_start_date, DateValidator.validate_date)

    def prompt_end_date(self) -> str:
        return self.prompt(self.view.prompt_end_date, DateValidator.validate_date)

    def prompt_tournament_pk(self) -> str:
        return self.view.prompt_tournament_pk()

    def prompt_round_match_winning_condition(self, chess_id: str) -> WinningCondition:
        user_input = self.view.prompt_round_match_winning_condition(chess_id)
        winning_condition = WinningCondition(user_input)
        return winning_condition

    def prompt_continue_setting_scores(self, round_name: str) -> bool:
        user_input = self.view.console.input(
            f"""New round beginned : {round_name} Continue to setting scores ?
                                             - 1 - Yes
                                             - 2 - No 
                                             Select : """
        )
        return True if user_input == "1" else False


class TournamentRenderHandler(CoreRenderer):

    def __init__(self, view: TournamentView) -> None:
        self.view = view

    def render_tournaments(self, tournaments: list[Tournament]) -> None:
        self.view.render_models(tournaments)

    def render_selected_tournament_name(self, tournament: Tournament) -> None:
        self.view.console.print(f"Selected tournament : {tournament.name}")
