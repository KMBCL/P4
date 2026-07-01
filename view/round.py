from view.core_view import CoreView
from models.round import Round

from core.constants import WinningCondition


class RoundView(CoreView[Round]):

    def prompt_round_match_winning_condition(self, chess_id: str) -> str:
        return self.console.input(
            f"""Enter match outcome for chess ID player '{chess_id}' :
            Choices are :
            - {WinningCondition.VICTORY} - Victory
            - {WinningCondition.DEFEAT} - Defeat
            - {WinningCondition.DRAW} - Draw
            Select : """
        )
