from __future__ import annotations

from typing import Any


from core.result import Result

from controllers.handlers.model_to_menu_item import ModelToMenuItem
from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)
from controllers.validators.menu import MenuValidator
from models.round import Round, RoundMatch
from models.tournament import Tournament
from service.tournament import TournamentService

from view.player import PlayerView
from view.round import RoundView

from menu.session_context import SessionContext


class TournamentSelector:

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.service = service

    def select_tournament_from_list(self, tournaments: list[Tournament]) -> Tournament:
        menu_items = ModelToMenuItem.tournament_to_menu_item(tournaments)
        self.renderer_handler.view.list_view.render_menu_items(menu_items)
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.list_view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        tournament = tournaments[int(user_input) - 1]
        return tournament

    def select_tournament_by_name(self) -> Result:
        prompted_name = self.prompt_handler.prompt_name()
        tournaments_result = self.service.get_tournament_by_name(prompted_name)
        if not tournaments_result:
            return tournaments_result

        tournaments: list[Tournament] = tournaments_result.required_value
        if len(tournaments) > 1:
            return Result.valid(value=self.select_tournament_from_list(tournaments))

        return Result.valid(value=tournaments[0])

    def select_tournament_by_stragegy(self, session_context: SessionContext) -> Result:
        if session_context.tournament_pk is not None:
            tournament_result = self.service.get_tournament_by_pk(
                session_context.required_tournament_pk
            )
            return tournament_result

        return self.select_tournament_by_name()

    def handle_tournament(self, session_context: SessionContext):
        tournament_result = Result.invalid(reason="initial loop")

        while not tournament_result:
            tournament_result = self.select_tournament_by_stragegy(session_context)
            if not tournament_result:
                self.renderer_handler.view.render_invalid_input(
                    reason=tournament_result.required_reason
                )

        tournament: Tournament = tournament_result.required_value
        session_context.tournament_pk = tournament.pk
        self.renderer_handler.render_selected_tournament_name(tournament)
        tournament.get_player_scores()

    def change_tournament(self, session_context: SessionContext) -> None:
        session_context.tournament_pk = None
        self.handle_tournament(session_context)


class TournamentRunner:

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.service = service

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

    def should_continue_setting_scores(self, next_round_name: str) -> Result:
        user_input = self.prompt_handler.prompt_continue_setting_scores(next_round_name)
        return Result.valid() if user_input == "1" else Result.invalid("Stopped")

    def run_setting_scores(self, next_round: Round, tournament: Tournament) -> None:
        incomplete_scores: list[RoundMatch] = self.service.extract_incomplete_matches(
            next_round
        )
        if not incomplete_scores:
            return None

        self.renderer_handler.view.render_setting_scores_for_round(next_round.name)
        self.set_incomplete_scores(incomplete_scores, tournament)

    def should_continue(self, round: Round) -> Result:
        should_continue_result = self.should_continue_setting_scores(round.name)
        if not should_continue_result:
            return should_continue_result

        return Result.valid(value=round)

    def run_tournament(self, session_context: SessionContext):
        tournament_result = self.service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        if not tournament_result:
            self.renderer_handler.view.render_invalid_input(
                tournament_result.required_reason
            )
            return None

        tournament: Tournament = tournament_result.required_value
        running_result = self.service.prepare_next_round(tournament)
        while running_result:
            next_round: Round = running_result.required_value
            self.run_setting_scores(next_round, tournament)
            next_round_result = self.service.prepare_next_round(tournament)
            if not next_round_result:
                self.renderer_handler.view.render_invalid_input(
                    tournament_result.required_reason
                )
                continue
            next_round = next_round_result.required_value
            running_result = self.should_continue(next_round)


class TournamentPlayer:

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.service = service

    def register_player(self, session_context: SessionContext) -> None:
        tournament_result = self.service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        tournament: Tournament = tournament_result.required_value
        if tournament.has_begun:
            self.renderer_handler.view.render_invalid_input(
                reason="Tournament already begun"
            )
            return

        user_input = self.prompt_handler.get_player_registration_input()
        result = self.service.register_player_to_tournament(
            tournament_pk=session_context.required_tournament_pk,
            chess_id=user_input,
        )

        if not result:
            self.renderer_handler.view.render_invalid_input(
                reason=result.required_reason
            )

    def show_register_players(self, session_context: SessionContext) -> None:
        registered_players_result = self.service.get_registered_players(
            tournament_pk=session_context.required_tournament_pk
        )

        player_view = PlayerView(console=self.renderer_handler.view.console)
        player_view.list_view.render_models(registered_players_result.required_value)


class TournamentRounds:

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.service = service

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
        round_view.list_view.render_models(tournament_rounds)


class TournamentController:
    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.service = service

    def create_new_tournament(self) -> None:
        self.service.repository.save_new_model(
            user_input=self.prompt_handler.get_tournament_input()
        )

    def show_tournaments(self) -> None:
        tournaments = self.service.repository.get_models()
        self.renderer_handler.render_tournaments(tournaments)

    def show_filtered_tournaments(self) -> None:
        pass
