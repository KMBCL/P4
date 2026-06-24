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
from models.player import Player
from service.tournament import TournamentService
from service.player import PlayerService

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
        if not running_result:
            self.renderer_handler.view.render_invalid_input(
                running_result.required_reason
            )

        while running_result:
            next_round: Round = running_result.required_value
            self.run_setting_scores(next_round, tournament)
            next_round_result = self.service.prepare_next_round(tournament)
            if not next_round_result:
                self.renderer_handler.view.render_invalid_input(
                    next_round_result.required_reason
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
        player_service: PlayerService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.service = service
        self.player_service = player_service

    def select_player_from_list(self, players: list[Player]) -> Player:
        menu_items = ModelToMenuItem.player_to_menu_item(players)
        self.renderer_handler.view.list_view.render_menu_items(menu_items)
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.list_view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        player = players[int(user_input) - 1]
        return player

    def get_unregistered_players(
        self, user_input: str, players: list[Player], tournament: Tournament
    ) -> Result:
        unregistered_players: list[Player] = [
            player
            for player in players
            if player.chess_id not in tournament.registered_player_chess_ids
        ]
        if not unregistered_players:
            return Result.invalid(
                f"All players matching '{user_input}' are already register"
            )

        return Result.valid(value=unregistered_players)

    def select_player_by_name(self, tournament: Tournament):
        user_input = self.prompt_handler.get_player_registration_input()
        players_result = self.player_service.get_player_by_name(user_input)
        if not players_result:
            return players_result

        players: list[Player] = players_result.required_value
        unregistered_players_result = self.get_unregistered_players(
            user_input, players, tournament
        )
        if not unregistered_players_result:
            return unregistered_players_result

        unregistered_players: list[Player] = unregistered_players_result.required_value
        if len(unregistered_players) > 1:
            return Result.valid(
                value=self.select_player_from_list(unregistered_players)
            )

        return Result.valid(value=unregistered_players[0])

    def is_tournament_registration_open(self, tournament_pk: str) -> Result:
        tournament_result = self.service.get_tournament_by_pk(tournament_pk)
        tournament: Tournament = tournament_result.required_value
        if tournament.has_begun:
            return Result.invalid(reason="Registration is now closed")

        return Result.valid(value=tournament)

    def display_result(self, result: Result) -> None:
        if not result:
            self.renderer_handler.view.render_invalid_input(
                reason=result.required_reason
            )
            return None

        self.renderer_handler.view.render_success("Done !")

    def register_player(self, session_context: SessionContext) -> None:
        registration_open_result = self.is_tournament_registration_open(
            session_context.required_tournament_pk
        )
        if not registration_open_result:
            self.display_result(registration_open_result)
            return None

        tournament: Tournament = registration_open_result.required_value
        regsitration_result = Result.invalid(reason="initial loop")
        while not regsitration_result:
            regsitration_result = self.select_player_by_name(tournament)
            if not regsitration_result:
                self.display_result(regsitration_result)
                continue

            player: Player = regsitration_result.required_value
            regsitration_result = self.service.register_player_to_tournament(
                tournament_pk=session_context.required_tournament_pk,
                chess_id=player.chess_id,
            )

            if not regsitration_result:
                self.display_result(regsitration_result)
                continue

            self.display_result(regsitration_result)

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
