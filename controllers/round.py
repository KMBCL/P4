"""Runs the use cases of the rounds."""

from __future__ import annotations

from typing import TypeAlias
from datetime import datetime

from core.result import Result
from core.core_formats import DATE_TIME

from controllers.handlers.model_to_menu_item import ModelToMenuItem
from controllers.handlers.should_continue_to_menu_item import ShouldContinueToMenuItem
from controllers.handlers.round import RoundPromptHandler, RoundRendererHandler
from controllers.validators.menu import MenuValidator


from service.tournament import TournamentService, TournamentStandingsService
from service.round import RoundService

from models.tournament import Tournament
from models.round import Round, RoundMatch
from models.player import Player

Tournaments: TypeAlias = list[Tournament]


class RoundController:
    """Opens a round, collects the scores of its matches, and closes it."""

    def __init__(
        self,
        prompt_handler: RoundPromptHandler,
        renderer_handler: RoundRendererHandler,
        round_service: RoundService,
        tournament_service: TournamentService,
        tournament_standings_service: TournamentStandingsService,
    ) -> None:
        """Holds the handlers and the services the use cases are run with.

        Args:
            prompt_handler (RoundPromptHandler): The handler to prompt through.
            renderer_handler (RoundRendererHandler): The handler to print through.
            round_service (RoundService): The rules governing the rounds.
            tournament_service (TournamentService): The rules governing the
                tournaments, used to store the one being played.
            tournament_standings_service (TournamentStandingsService): The
                standings the players are paired by.
        """
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler
        self.round_service = round_service
        self.tournament_service = tournament_service
        self.tournament_standings_service = tournament_standings_service

    def get_incomplete_matches(self, round: Round) -> list[RoundMatch]:
        """Reads the matches of the round that hold no score yet.

        Args:
            round (Round): The round to read.

        Returns:
            list[RoundMatch]: The matches left to play.
        """
        return self.round_service.get_incomplete_round_matches(round)

    def select_round_match_winner(self, round_match: RoundMatch) -> Player | None:
        """Asks the user for the outcome of a match.

        Args:
            round_match (RoundMatch): The match to give an outcome to.

        Returns:
            Player | None: The player who won, or None for a draw.
        """
        menu_items = ModelToMenuItem.round_match_to_winning_condition_menu_item(
            round_match
        )
        self.renderer_handler.view.render_menu_items(menu_items)
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        selected_menu_item = menu_items[int(user_input) - 1]
        winner: Player | None = selected_menu_item.value
        return winner

    def set_incomplete_scores(
        self, round_matches: list[RoundMatch], tournament: Tournament
    ) -> None:
        """Asks the user for the outcome of every match left to play.

        The tournament is stored after each match, so that an interrupted round
        keeps the scores already given.

        Args:
            round_matches (list[RoundMatch]): The matches left to play.
            tournament (Tournament): The tournament to store.
        """
        for round_match in round_matches:
            winner = self.select_round_match_winner(round_match)
            round_match.set_score(winner)
            self.tournament_service.save_tournament(tournament)

    def should_continue_setting_scores(self, next_round_name: str) -> Result:
        """Asks the user  to play the round to come.

        Args:
            next_round_name (str): The name of the round to come.

        Returns:
            Result:
                - A valid result, holding no value, when the user goes on.
                - An invalid one when the user stops.
        """
        menu_items = ShouldContinueToMenuItem.should_continue_to_menu_item()
        self.renderer_handler.view.render_menu_items(
            menu_items, "Continue to set scores ?"
        )
        user_input = self.prompt_handler.prompt(
            self.prompt_handler.view.prompt_menu_choice,
            lambda user_input: MenuValidator.is_choice_in_range(user_input, menu_items),
        )
        selected_menu_item = menu_items[int(user_input) - 1]
        return Result.valid() if selected_menu_item.value else Result.invalid("Stopped")

    def prepare_next_round(self, tournament: Tournament) -> Result:
        """Pairs the round to come, and stores the tournament.

        Args:
            tournament (Tournament): The tournament to run.

        Returns:
            Result:
                - A valid result carrying the round to play.
                - An invalid one when every round is completed, or when the
                  players cannot be paired.
        """
        next_round_result = self.round_service.prepare_next_round(
            tournament,
            self.tournament_standings_service.get_players_by_standing(tournament),
        )
        if not next_round_result:
            return next_round_result

        self.tournament_service.save_tournament(tournament)
        return next_round_result

    def set_end_timestamp(self, round: Round, tournament: Tournament) -> None:
        """Sets when the round ended, once every match holds a score.

        Nothing is set while a match is left to play, nor when the round has
        already been closed.

        Args:
            round (Round): The round to close.
            tournament (Tournament): The tournament to store.
        """
        if self.get_incomplete_matches(round):
            return None

        if round.end_timestamp:
            return None

        round.end_timestamp = datetime.now().strftime(DATE_TIME)
        self.tournament_service.save_tournament(tournament)

    def set_start_timestamp(self, round: Round, tournament: Tournament) -> None:
        """Sets when the round started, unless it has already been opened.

        Args:
            round (Round): The round to open.
            tournament (Tournament): The tournament to store.
        """
        if round.start_timestamp:
            return None

        round.start_timestamp = datetime.now().strftime(DATE_TIME)
        self.tournament_service.save_tournament(tournament)
