from __future__ import annotations

from typing import TYPE_CHECKING

from core.core_controller import CoreController
from core.constants import WinningCondition

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)
from models.tournament import Tournament
from service.tournament import TournamentService

from view.player import PlayerView
from view.round import RoundView

from models.round import Round, RoundMatch

from menu.session_context import SessionContext


class TournamentController(
    CoreController[
        TournamentPromptHandler,
        TournamentRenderHandler,
    ]
):
    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
    ) -> None:
        super().__init__(prompt_handler, renderer_handler)
        self.service = TournamentService()

    def get_tournament(self, tournament_pk: str) -> Tournament | None:
        tournament_result = self.service.get_tournament_by_pk(tournament_pk)
        if not tournament_result:
            self.renderer_handler.view.render_invalid_input(
                reason=tournament_result.required_reason
            )
            return

        return tournament_result.required_value

    def create_new_tournament(self) -> None:
        self.service.repository.save_new_model(
            user_input=self.prompt_handler.get_tournament_input()
        )

    def register_player(self, session_context: SessionContext) -> None:
        user_input = self.prompt_handler.get_player_registration_input()
        result = self.service.register_player_to_tournament(
            tournament_pk=user_input.tournament_pk,
            chess_id=user_input.chess_id,
        )

        if not result:
            self.renderer_handler.view.render_invalid_input(
                reason=result.required_reason
            )

    def show_tournaments(self) -> None:
        tournaments = self.service.repository.get_models()
        self.renderer_handler.render_tournaments(tournaments)

    def show_filtered_tournaments(self) -> None:
        pass

    def show_register_players(self, session_context: SessionContext) -> None:
        registered_players_result = self.service.get_registered_players(
            tournament_pk=session_context.required_tournament_pk
        )

        player_view = PlayerView(console=self.renderer_handler.view.console)
        player_view.render_models(registered_players_result.required_value)

    def show_tournament_rounds(self) -> None:
        user_input = self.prompt_handler.get_tournament_pk_input()
        result = self.service.get_tournament_rounds(tournament_pk=user_input)
        if not result:
            self.renderer_handler.view.render_invalid_input(
                reason=result.required_reason
            )
            return

        tournament_rounds = result.required_value
        round_view = RoundView(console=self.renderer_handler.view.console)
        round_view.render_models(tournament_rounds)

    def handle_tournament(self, session_context: SessionContext):
        tournament = self.get_tournament(
            session_context.tournament_pk
            or self.prompt_handler.get_tournament_pk_input()
        )
        if tournament is None:
            return None

        session_context.tournament_pk = tournament.pk
        self.renderer_handler.render_selected_tournament_name(tournament)

    def change_tournament(self, session_context: SessionContext) -> None:
        session_context.tournament_pk = None
        self.handle_tournament(session_context)

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
            self.service.save_tournament(tournament)

    def should_continue_setting_scores(
        self, is_first_score_input: bool, next_round_name: str
    ) -> bool:
        if not is_first_score_input:
            return self.prompt_handler.prompt_continue_setting_scores(next_round_name)

        return True

    def run_setting_scores(self, next_round: Round, tournament: Tournament) -> bool:
        incomplete_scores: list[RoundMatch] = self.service.extract_incomplete_matches(
            next_round
        )
        if not incomplete_scores:
            return False

        self.renderer_handler.view.render_setting_scores_for_round(next_round.name)
        self.set_incomplete_scores(incomplete_scores, tournament)

        return True

    def run_tournament(self, session_context: SessionContext):
        tournament = self.get_tournament(session_context.required_tournament_pk)
        if tournament is None:
            return None

        running = True
        is_first_score_input = True
        while running:
            next_round_result = self.service.prepare_next_round(tournament)
            if not next_round_result:
                running = next_round_result
                self.renderer_handler.view.render_invalid_input(
                    next_round_result.required_reason
                )
                continue

            next_round: Round = next_round_result.required_value
            running = self.should_continue_setting_scores(
                is_first_score_input, next_round.name
            )
            if not running:
                continue

            scores_were_set = self.run_setting_scores(next_round, tournament)
            if not scores_were_set:
                continue

            is_first_score_input = False
