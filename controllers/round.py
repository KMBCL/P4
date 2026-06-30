from __future__ import annotations

from typing import TypeAlias

from core.result import Result

from controllers.handlers.round import RoundPromptHandler, RoundRenderHandler
from service.tournament import TournamentService
from service.round import RoundService

from models.tournament import Tournament
from models.round import Round, RoundMatch

Tournaments: TypeAlias = list[Tournament]


class RoundController:

    def __init__(
        self,
        prompt_handler: RoundPromptHandler,
        render_handler: RoundRenderHandler,
        round_service: RoundService,
        tournament_service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.render_handler = render_handler
        self.round_service = round_service
        self.tournament_service = tournament_service

    def save_round_players(self, tournament: Tournament, round: Round) -> Result:
        tournament_result = self.round_service.set_round_players(
            tournament=tournament, round=round
        )
        self.tournament_service.save_tournament(tournament)
        return tournament_result

    def get_incomplete_matches(self, round: Round) -> list[RoundMatch]:
        incomplete_scores: list[RoundMatch] = []
        if not round.is_round_score_complete():
            incomplete_scores = [
                round_match
                for round_match in round.round_matches
                if not round_match.is_score_complete()
            ]
        return incomplete_scores

    def set_incomplete_scores(
        self, round_matches: list[RoundMatch], tournament: Tournament
    ) -> None:
        for round_match in round_matches:
            winning_condition = (
                self.prompt_handler.prompt_round_match_winning_condition(
                    round_match.score_a.chess_id
                )
            )
            round_match.set_score(winning_condition)
            self.tournament_service.save_tournament(tournament)

    def should_continue_setting_scores(self, next_round_name: str) -> Result:
        user_input = self.prompt_handler.prompt_continue_setting_scores(next_round_name)
        return Result.valid() if user_input == "1" else Result.invalid("Stopped")

    def prepare_next_round(self, tournament: Tournament) -> Result:
        return self.round_service.prepare_next_round(tournament)
