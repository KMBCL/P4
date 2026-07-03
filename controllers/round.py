from __future__ import annotations

from typing import TypeAlias

from core.result import Result

from controllers.handlers.model_to_menu_item import ModelToMenuItem
from controllers.handlers.should_continue_to_menu_item import ShouldContinueToMenuItem
from controllers.handlers.round import RoundPromptHandler, RoundRenderHandler
from controllers.validators.menu import MenuValidator

from service.tournament import TournamentService, TournamentStandingsService
from service.round import RoundService

from models.tournament import Tournament
from models.round import Round, RoundMatch
from models.player import Player

Tournaments: TypeAlias = list[Tournament]


class RoundController:

    def __init__(
        self,
        prompt_handler: RoundPromptHandler,
        renderer_handler: RoundRenderHandler,
        round_service: RoundService,
        tournament_service: TournamentService,
        tournament_standings_service: TournamentStandingsService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.round_service = round_service
        self.tournament_service = tournament_service
        self.tournament_standings_service = tournament_standings_service

    def get_incomplete_matches(self, round: Round) -> list[RoundMatch]:
        return self.round_service.get_incomplete_round_matches(round)

    def select_round_match_winner(self, round_match: RoundMatch) -> Player | None:
        menu_items = ModelToMenuItem.round_match_to_winning_condition_menu_item(
            round_match
        )
        self.renderer_handler.view.list_view.render_menu_items(menu_items)
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.list_view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        selected_menu_item = menu_items[int(user_input) - 1]
        winner: Player | None = selected_menu_item.value
        return winner

    def set_incomplete_scores(
        self, round_matches: list[RoundMatch], tournament: Tournament
    ) -> None:
        for round_match in round_matches:
            winner = self.select_round_match_winner(round_match)
            round_match.set_score(winner)
            self.tournament_service.save_tournament(tournament)

    def should_continue_setting_scores(self, next_round_name: str) -> Result:
        menu_items = ShouldContinueToMenuItem.should_continue_to_menu_item()
        self.renderer_handler.view.list_view.render_menu_items(menu_items)
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.list_view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        selected_menu_item = menu_items[int(user_input) - 1]
        return Result.valid() if selected_menu_item.value else Result.invalid("Stopped")

    def prepare_next_round(self, tournament: Tournament) -> Result:
        next_round_result = self.round_service.prepare_next_round(
            tournament,
            self.tournament_standings_service.get_players_by_standing(tournament),
        )
        if not next_round_result:
            return next_round_result

        self.tournament_service.save_tournament(tournament)
        return next_round_result
