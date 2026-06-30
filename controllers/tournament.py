from __future__ import annotations

from core.result import Result

from controllers.handlers.model_to_menu_item import ModelToMenuItem
from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRenderHandler,
)
from controllers.validators.menu import MenuValidator
from controllers.round import RoundController
from models.round import Round, RoundMatch
from models.tournament import Tournament
from models.player import Player

from service.tournament import TournamentService
from service.player import PlayerService


from view.player import PlayerView


from menu.session_context import SessionContext


class TournamentSelector:

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        tournament_service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service

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
        tournaments_result = self.tournament_service.get_tournament_by_name(
            prompted_name
        )
        if not tournaments_result:
            return tournaments_result

        tournaments: list[Tournament] = tournaments_result.get_value()
        if len(tournaments) > 1:
            return Result.valid(value=self.select_tournament_from_list(tournaments))

        return Result.valid(value=tournaments[0])

    def use_cache(self, session_context: SessionContext) -> Result | None:
        if session_context.tournament_pk is None:
            return None

        tournament_result = self.tournament_service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        return tournament_result

    def select_tournament(self, session_context: SessionContext) -> Result:
        cached_tournament_result = self.use_cache(session_context)
        if cached_tournament_result is not None:
            return cached_tournament_result

        return self.select_tournament_by_name()

    def handle_tournament(self, session_context: SessionContext):
        tournament_result = Result.invalid(reason="initial loop")

        while not tournament_result:
            tournament_result = self.select_tournament(session_context)
            if not tournament_result:
                self.renderer_handler.view.render_invalid_input(
                    reason=tournament_result.get_reason()
                )

        tournament: Tournament = tournament_result.get_value()
        session_context.tournament_pk = tournament.pk
        self.renderer_handler.render_selected_tournament_name(tournament)

    def change_tournament(self, session_context: SessionContext) -> None:
        session_context.tournament_pk = None
        self.handle_tournament(session_context)


class TournamentRunner:

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        tournament_service: TournamentService,
        round_controller: RoundController,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service
        self.round_controller = round_controller

    def run_setting_scores(self, next_round: Round, tournament: Tournament) -> None:
        incomplete_scores: list[RoundMatch] = (
            self.round_controller.get_incomplete_matches(next_round)
        )
        if not incomplete_scores:
            return None

        self.renderer_handler.view.render_setting_scores_for_round(next_round.name)
        self.round_controller.set_incomplete_scores(incomplete_scores, tournament)

    def should_continue(self, round: Round) -> Result:
        should_continue_result = self.round_controller.should_continue_setting_scores(
            round.name
        )
        if not should_continue_result:
            return should_continue_result

        return Result.valid(value=round)

    def run_tournament(self, session_context: SessionContext):
        tournament_result = self.tournament_service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        if not tournament_result:
            self.renderer_handler.view.render_invalid_input(
                tournament_result.get_reason()
            )
            return None

        tournament: Tournament = tournament_result.get_value()
        running_result = self.round_controller.prepare_next_round(tournament)
        if not running_result:
            self.renderer_handler.view.render_invalid_input(running_result.get_reason())

        while running_result:
            next_round: Round = running_result.get_value()
            self.run_setting_scores(next_round, tournament)
            running_result = self.round_controller.prepare_next_round(tournament)
            if not running_result:
                self.renderer_handler.view.render_invalid_input(
                    running_result.get_reason()
                )
                continue

            next_round = running_result.get_value()
            running_result = self.should_continue(next_round)


class TournamentPlayer:

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        tournament_service: TournamentService,
        player_service: PlayerService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service
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

    def select_player_by_name(self, tournament: Tournament):
        user_input = self.prompt_handler.get_player_registration_input()
        players_result = self.player_service.get_player_by_name(user_input)
        if not players_result:
            return players_result

        players: list[Player] = players_result.get_value()
        unregistered_players_result = self.player_service.get_unregistered_players(
            user_input, players, tournament
        )
        if not unregistered_players_result:
            return unregistered_players_result

        unregistered_players: list[Player] = unregistered_players_result.get_value()
        if len(unregistered_players) > 1:
            return Result.valid(
                value=self.select_player_from_list(unregistered_players)
            )

        return Result.valid(value=unregistered_players[0])

    def is_tournament_registration_open(self, tournament_pk: str) -> Result:
        tournament_result = self.tournament_service.get_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        tournament: Tournament = tournament_result.get_value()
        if self.tournament_service.has_begun(tournament):
            return Result.invalid(reason="Registration is now closed")

        return Result.valid(value=tournament)

    def display_result(self, result: Result) -> None:
        if not result:
            self.renderer_handler.view.render_invalid_input(reason=result.get_reason())
            return None

        self.renderer_handler.view.render_success("Done !")

    def register_player(self, session_context: SessionContext) -> None:
        registration_open_result = self.is_tournament_registration_open(
            session_context.required_tournament_pk
        )
        if not registration_open_result:
            self.display_result(registration_open_result)
            return None

        tournament: Tournament = registration_open_result.get_value()
        regsitration_result = Result.invalid(reason="initial loop")
        while not regsitration_result:
            regsitration_result = self.select_player_by_name(tournament)
            if not regsitration_result:
                self.display_result(regsitration_result)
                continue

            player: Player = regsitration_result.get_value()
            regsitration_result = self.tournament_service.register_player_to_tournament(
                tournament_pk=session_context.required_tournament_pk,
                chess_id=player.chess_id,
            )

            if not regsitration_result:
                self.display_result(regsitration_result)
                continue

            self.display_result(regsitration_result)

    def show_register_players(self, session_context: SessionContext) -> None:
        registered_players_result = self.tournament_service.get_registered_players(
            tournament_pk=session_context.required_tournament_pk
        )
        if not registered_players_result:
            self.renderer_handler.view.render_invalid_input(
                registered_players_result.get_reason()
            )
            return None

        player_view = PlayerView(console=self.renderer_handler.view.console)
        player_view.list_view.render_models(registered_players_result.get_value())


class TournamentController:
    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRenderHandler,
        tournament_service: TournamentService,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service

    def create_new_tournament(self) -> None:
        user_input = self.prompt_handler.get_tournament_input()
        create_result = self.tournament_service.create_tournament(user_input)
        if not create_result:
            self.renderer_handler.view.render_invalid_input(create_result.get_reason())
            return None

        self.renderer_handler.view.render_success(create_result.get_success_message())

    def show_tournaments(self) -> None:
        tournaments_result = self.tournament_service.get_tournaments()
        if not tournaments_result:
            self.renderer_handler.view.render_invalid_input(
                tournaments_result.get_reason()
            )
            return None

        tournaments: list[Tournament] = tournaments_result.get_value()
        self.renderer_handler.render_tournaments(tournaments)
