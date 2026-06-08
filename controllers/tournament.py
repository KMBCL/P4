from __future__ import annotations

from typing import TYPE_CHECKING

from core.core_controller import CoreController

from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)

from service.tournament import TournamentService

from view.player import PlayerView
from view.round import RoundView

from models.round import Round, RoundMatch


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

    def create_new_tournament(self) -> None:
        self.service.repository.save_new_model(
            user_input=self.prompt_handler.get_tournament_input()
        )

    def register_player(self) -> None:
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

    def show_tournament_players(self) -> None:
        user_input = self.prompt_handler.get_tournament_pk_input()
        registered_players_result = self.service.get_registered_players(
            tournament_pk=user_input
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

    def set_round_matches(self) -> None:
        tournament_pk_input = self.prompt_handler.get_tournament_pk_input()
        round_name_input = self.prompt_handler.get_round_name()

        result = self.service.set_round_matches(
            tournament_pk=tournament_pk_input, round_name=round_name_input
        )
        if not result:
            self.renderer_handler.view.render_invalid_input(
                reason=result.required_reason
            )
            return

    def auto_score_b(self, score_a: float) -> float:
        if score_a == 1:
            return 0
        if score_a == 0.5:
            return 0.5

        return 1

    def set_matches_scores(self) -> None:
        tournament_pk_input = self.prompt_handler.get_tournament_pk_input()
        round_name_input = self.prompt_handler.get_round_name()

        round_matches_result = self.service.get_round_matches(
            tournament_pk_input, round_name_input
        )
        if not round_matches_result:
            self.renderer_handler.view.render_invalid_input(
                reason=round_matches_result.required_reason
            )
            return

        round_matches: list[RoundMatch] = round_matches_result.required_value
        for round_match in round_matches:
            print("round match", round_match)
            print("Display chess id", round_match.score_a.chess_id)
            round_match.score_a.score_value = float(input("Enter player's score : "))
            round_match.score_b.score_value = self.auto_score_b(
                round_match.score_a.score_value
            )

        self.service.save_round_matches(
            round_matches,
            tournament_pk_input,
            round_name_input,
        )
