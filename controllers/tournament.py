"""Runs the use cases of the tournaments."""

from __future__ import annotations

from core.result import Result

from controllers.handlers.model_to_menu_item import ModelToMenuItem
from controllers.handlers.tournament import (
    TournamentPromptHandler,
    TournamentRendererHandler,
)
from controllers.handlers.player import PlayerRendererHandler

from controllers.validators.menu import MenuValidator
from controllers.round import RoundController
from models.round import Round, RoundMatch
from models.tournament import Tournament
from models.player import Player

from service.tournament import TournamentService, TournamentStandingsService
from service.player import PlayerService
from service.helpers.sort import sort_players_by_last_name


from menu.session_context import SessionContext


class TournamentSelector:
    """Selects the tournament."""

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRendererHandler,
        tournament_service: TournamentService,
    ) -> None:
        """Holds the handlers and the service the use cases are run with.

        Args:
            prompt_handler (TournamentPromptHandler): The handler to prompt through.
            renderer_handler (TournamentRendererHandler): The handler to print through.
            tournament_service (TournamentService): The rules governing the
                tournaments.
        """
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service

    def select_tournament_from_list(self, tournaments: list[Tournament]) -> Tournament:
        """Asks the user to pick one tournament out of several.

        Args:
            tournaments (list[Tournament]): The tournaments to pick from.

        Returns:
            Tournament: The tournament the user picked.
        """
        menu_items = ModelToMenuItem.tournament_to_menu_item(tournaments)
        self.renderer_handler.view.render_menu_items(menu_items)
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        tournament = tournaments[int(user_input) - 1]
        return tournament

    def select_tournament_by_name(self) -> Result:
        """Asks for a name, and for a choice when several names match.

        Args:
            None

        Returns:
            Result:
                - A valid result carrying the selected tournament.
                - An invalid one when no name matches.
        """
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
        """Reads the tournament the user already selected, if there is one.

        Args:
            session_context (SessionContext): The selections of the user.

        Returns:
            Result | None: The result of reading the selected tournament, or None
                when no tournament is selected yet.
        """
        if session_context.tournament_pk is None:
            return None

        tournament_result = self.tournament_service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        return tournament_result

    def select_tournament(self, session_context: SessionContext) -> Result:
        """Reads the selected tournament, and asks for one when there is none.

        Args:
            session_context (SessionContext): The selections of the user.

        Returns:
            Result:
                - A valid result carrying the selected tournament.
                - An invalid one when no name matches.
        """
        cached_tournament_result = self.use_cache(session_context)
        if cached_tournament_result is not None:
            return cached_tournament_result

        return self.select_tournament_by_name()

    def handle_tournament(self, session_context: SessionContext) -> None:
        """Selects a tournament, asking again until one is found.

        The selected tournament is kept in the session, so that every later
        action works on it without asking again.

        Args:
            session_context (SessionContext): The selections of the user.
        """
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
        """Drops the selected tournament, and selects another one.

        Args:
            session_context (SessionContext): The selections of the user.
        """
        session_context.tournament_pk = None
        self.handle_tournament(session_context)


class TournamentRunner:
    """Plays a tournament, one round after the other."""

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRendererHandler,
        tournament_service: TournamentService,
        round_controller: RoundController,
    ) -> None:
        """Holds the handlers, the service and the controller of the rounds.

        Args:
            prompt_handler (TournamentPromptHandler): The handler to prompt through.
            renderer_handler (TournamentRendererHandler): The handler to print through.
            tournament_service (TournamentService): The rules governing the
                tournaments.
            round_controller (RoundController): The use cases of the rounds.
        """
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service
        self.round_controller = round_controller

    def run_setting_scores(self, next_round: Round, tournament: Tournament) -> None:
        """Collects the outcome of every match left to play in the round.

        Args:
            next_round (Round): The round being played.
            tournament (Tournament): The tournament to store.
        """
        incomplete_scores: list[RoundMatch] = (
            self.round_controller.get_incomplete_matches(next_round)
        )
        if not incomplete_scores:
            return None

        self.renderer_handler.view.render_setting_scores_for_round(next_round.name)
        self.round_controller.set_incomplete_scores(incomplete_scores, tournament)

    def should_continue(self, round: Round) -> Result:
        """Asks the user if to play the round to come.

        Args:
            round (Round): The round to come.

        Returns:
            Result:
                - A valid result carrying the round, when the user goes on.
                - An invalid one when the user stops.
        """
        should_continue_result = self.round_controller.should_continue_setting_scores(
            round.name
        )
        if not should_continue_result.is_valid():
            return should_continue_result

        return Result.valid(value=round)

    def run_setting_start_round(self, round: Round, tournament: Tournament) -> None:
        """Opens the round, asking when it started.

        Args:
            round (Round): The round to open.
            tournament (Tournament): The tournament to store.
        """
        self.round_controller.set_start_timestamp(round, tournament)

    def run_setting_end_round(self, round: Round, tournament: Tournament) -> None:
        """Closes the round, asking when it ended.

        Args:
            round (Round): The round to close.
            tournament (Tournament): The tournament to store.
        """
        self.round_controller.set_end_timestamp(round, tournament)

    def run_tournament(self, session_context: SessionContext):
        """Plays the selected tournament, until it ends or the user stops.

        Each round is opened, played and closed, and the user is asked if to
        go on before the next one is played.

        Args:
            session_context (SessionContext): The selections of the user.
        """
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
            self.renderer_handler.render_playing_round(next_round)
            self.run_setting_start_round(next_round, tournament)
            self.run_setting_scores(next_round, tournament)
            self.run_setting_end_round(next_round, tournament)
            running_result = self.round_controller.prepare_next_round(tournament)
            if not running_result:
                self.renderer_handler.view.render_invalid_input(
                    running_result.get_reason()
                )
                continue

            next_round = running_result.get_value()
            running_result = self.should_continue(next_round)


class TournamentPlayer:
    """Registers the players to a tournament, and shows the registered ones."""

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRendererHandler,
        tournament_service: TournamentService,
        player_service: PlayerService,
        player_renderer_handler: PlayerRendererHandler,
    ) -> None:
        """Holds the handlers and the services the use cases are run with.

        Args:
            prompt_handler (TournamentPromptHandler): The handler to prompt through.
            renderer_handler (TournamentRendererHandler): The handler to print through.
            tournament_service (TournamentService): The rules governing the
                tournaments.
            player_service (PlayerService): The rules governing the players.
            player_renderer_handler (PlayerRendererHandler): The handler printing the
                players.
        """
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service
        self.player_service = player_service
        self.player_renderer_handler = player_renderer_handler

    def select_player_from_list(self, players: list[Player]) -> Player:
        """Asks the user to pick one player out of several.

        Args:
            players (list[Player]): The players to pick from.

        Returns:
            Player: The player the user picked.
        """
        menu_items = ModelToMenuItem.player_to_menu_item(players)
        self.renderer_handler.view.render_menu_items(menu_items)
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        player = players[int(user_input) - 1]
        return player

    def select_player_by_name(self, tournament: Tournament):
        """Asks for a last name, and for a choice when several players match.

        Only the players not registered yet are offered.

        Args:
            tournament (Tournament): The tournament to register to.

        Returns:
            Result:
                - A valid result carrying the selected player.
                - An invalid one when no last name matches, or when every
                  matching player is already registered.
        """
        user_input = self.prompt_handler.get_player_registration_input()
        players_result = self.player_service.get_player_by_name(user_input)
        if not players_result:
            return players_result

        players: list[Player] = players_result.get_value()
        unregistered_players_result = self.player_service.get_unregistered_players(
            players, tournament
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
        """Tells if the tournament still accepts a registration.

        Registration closes as soon as the tournament has been played.

        Args:
            tournament_pk (str): The primary key of the tournament.

        Returns:
            Result:
                - A valid result carrying the tournament.
                - An invalid one when no tournament holds that primary key, or
                  when it has already begun.
        """
        tournament_result = self.tournament_service.get_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        tournament: Tournament = tournament_result.get_value()

        if self.tournament_service.has_begun(tournament):
            return Result.invalid(reason="Registration is now closed")

        return Result.valid(value=tournament)

    def display_result(self, result: Result) -> None:
        """Tells the user how the registration went.

        Args:
            result (Result): The outcome to tell.
        """
        if not result:
            self.renderer_handler.view.render_invalid_input(reason=result.get_reason())
            return None

        self.renderer_handler.view.render_success("Done !")

    def register_player(self, session_context: SessionContext) -> None:
        """Registers players to the selected tournament, one after the other.

        Args:
            session_context (SessionContext): The selections of the user.
        """
        registration_open_result = self.is_tournament_registration_open(
            session_context.required_tournament_pk
        )
        if not registration_open_result:
            self.display_result(registration_open_result)
            return None

        tournament: Tournament = registration_open_result.get_value()

        player_left_result = self.tournament_service.check_players_left(tournament)
        if not player_left_result:
            self.display_result(player_left_result)
            return None

        registration_result = Result.invalid(reason="initial loop")
        while not registration_result:
            registration_result = self.select_player_by_name(tournament)
            if not registration_result:
                self.display_result(registration_result)
                continue

            player: Player = registration_result.get_value()
            registration_result = self.tournament_service.register_player_to_tournament(
                tournament, player
            )

            if not registration_result:
                self.display_result(registration_result)
                continue

            self.display_result(registration_result)

    def show_register_players(self, session_context: SessionContext) -> None:
        """Prints the players registered to the selected tournament.

        Args:
            session_context (SessionContext): The selections of the user.
        """
        registered_players_result = self.tournament_service.get_registered_players(
            tournament_pk=session_context.required_tournament_pk
        )
        if not registered_players_result:
            self.renderer_handler.view.render_invalid_input(
                registered_players_result.get_reason()
            )
            return None

        self.player_renderer_handler.render_players(
            sort_players_by_last_name(registered_players_result.get_value())
        )


class TournamentController:
    """Creates the tournaments, and shows what they hold."""

    def __init__(
        self,
        prompt_handler: TournamentPromptHandler,
        renderer_handler: TournamentRendererHandler,
        tournament_service: TournamentService,
        tournament_standings_service: TournamentStandingsService,
    ) -> None:
        """Holds the handlers and the services the use cases are run with.

        Args:
            prompt_handler (TournamentPromptHandler): The handler to prompt through.
            renderer_handler (TournamentRendererHandler): The handler to print through.
            tournament_service (TournamentService): The rules governing the
                tournaments.
            tournament_standings_service (TournamentStandingsService): The
                standings of a tournament.
        """
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.tournament_service = tournament_service
        self.tournament_standings_service = tournament_standings_service

    def create_new_tournament(self) -> None:
        """Asks for a tournament, stores it, and tells the user how it went."""
        user_input = self.prompt_handler.get_tournament_input()
        create_result = self.tournament_service.create_tournament(user_input)
        if not create_result:
            self.renderer_handler.view.render_invalid_input(create_result.get_reason())
            return None

        self.renderer_handler.view.render_success(create_result.get_success_message())

    def show_tournaments(self) -> None:
        """Prints every stored tournament."""
        tournaments_result = self.tournament_service.get_tournaments()
        if not tournaments_result:
            self.renderer_handler.view.render_invalid_input(
                tournaments_result.get_reason()
            )
            return None

        tournaments: list[Tournament] = tournaments_result.get_value()
        self.renderer_handler.render_tournaments(tournaments)

    def show_standings(self, session_context: SessionContext):
        """Prints the standings of the selected tournament.

        Nothing is printed of a tournament that has yet to be played.

        Args:
            session_context (SessionContext): The selections of the user.
        """
        tournament_result = self.tournament_service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        if not tournament_result:
            self.renderer_handler.view.render_invalid_input(
                tournament_result.get_reason()
            )
            return None

        tournament: Tournament = tournament_result.get_value()
        if not self.tournament_service.has_begun(tournament):
            self.renderer_handler.view.render_invalid_input(
                "Tournament not begun yet. No standings to show."
            )
            return None

        standings = self.tournament_standings_service.get_tournament_standings(
            tournament
        )
        self.renderer_handler.render_standings(standings)

    def show_tournament_details(self, session_context: SessionContext) -> None:
        """Prints the fields of the selected tournament.

        Args:
            session_context (SessionContext): The selections of the user.
        """
        tournament_result = self.tournament_service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        if not tournament_result:
            self.renderer_handler.view.render_invalid_input(
                tournament_result.get_reason()
            )
            return None

        tournament: Tournament = tournament_result.get_value()
        self.renderer_handler.render_tournament_details(tournament)

    def show_tournament_rounds(self, session_context: SessionContext) -> None:
        """Prints every round of the selected tournament, and their matches.

        Args:
            session_context (SessionContext): The selections of the user.
        """
        tournament_result = self.tournament_service.get_tournament_by_pk(
            session_context.required_tournament_pk
        )
        if not tournament_result:
            self.renderer_handler.view.render_invalid_input(
                tournament_result.get_reason()
            )
            return None

        tournament: Tournament = tournament_result.get_value()
        self.renderer_handler.render_tournament_rounds(tournament)
