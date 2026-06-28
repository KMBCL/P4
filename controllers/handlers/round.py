from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler
from core.constants import WinningCondition

from view.round import RoundView


class RoundPromptHandler(CorePromptHandler[RoundView]):

    def prompt_round_match_winning_condition(self, chess_id: str) -> WinningCondition:
        user_input = self.view.prompt_round_match_winning_condition(chess_id)
        winning_condition = WinningCondition(user_input)
        return winning_condition

    def prompt_continue_setting_scores(self, round_name: str) -> str:
        user_input = self.view.console.input(
            f"""New round beginned : {round_name} Continue to setting scores ?
                                             - 1 - Yes
                                             - 2 - No 
                                             Select : """
        )
        return "YES" if user_input == "1" else "NO"


class RoundRenderHandler(CoreRenderer):

    def __init__(self, view: RoundView) -> None:
        self.view = view
