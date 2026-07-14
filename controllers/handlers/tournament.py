"""Prompts and renders the tournaments, their standings and their rounds."""

from core.color import ColorHelper, RoundMatchcolor, Formatter, TournamentFormatter
from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler

from view.tournament import TournamentView
from controllers.validators.date import DateValidator

from models.tournament import Tournament, TournamentInputData
from models.round import Round, RoundMatch
from models.score import TournamentPlayerScore


class TournamentPromptHandler(CorePromptHandler[TournamentView]):
    """Asks the user for a tournament, validating the fields that have a format."""

    def get_tournament_input(self):
        """Asks the user for every field of a tournament.

        Returns:
            TournamentInputData: The raw fields, ready to be given to the service.
        """
        self.view.skip_line()
        return TournamentInputData(
            name=self.prompt_name(),
            place=self.prompt_place(),
            start_date=self.prompt_start_date(),
            end_date=self.prompt_end_date(),
            description=self.prompt_description(),
            round_count=self.prompt_round_count(),
        )

    def get_player_registration_input(self):
        """Asks for the last name of the player to register.

        Returns:
            str: The raw last name, unvalidated.
        """
        return self.view.prompt_register_player()

    def prompt_name(self) -> str:
        """Asks for the name, which has no format to validate.

        Returns:
            str: The raw name, unvalidated.
        """
        return self.view.prompt_name()

    def prompt_place(self) -> str:
        """Asks for the place, which has no format to validate.

        Returns:
            str: The raw place, unvalidated.
        """
        return self.view.prompt_place()

    def prompt_description(self) -> str:
        """Asks for the description, which has no format to validate.

        Returns:
            str: The raw description, unvalidated.
        """
        return self.view.prompt_description()

    def prompt_round_count(self) -> str:
        """Asks for the round count, which has no format to validate.

        Returns:
            str: The raw round count, unvalidated. An empty input keeps the
                default.
        """
        return self.view.prompt_round_count()

    def prompt_start_date(self) -> str:
        """Asks for the start date, until its format is the expected one.

        Returns:
            str: The raw date, once validated.
        """
        return self.prompt(self.view.prompt_start_date, DateValidator.validate_date)

    def prompt_end_date(self) -> str:
        """Asks for the end date, until its format is the expected one.

        Returns:
            str: The raw date, once validated.
        """
        return self.prompt(self.view.prompt_end_date, DateValidator.validate_date)


class TournamentRenderHandler(CoreRenderer):
    """Prints the tournaments, their standings, their rounds and their matches."""

    def __init__(self, view: TournamentView) -> None:
        """Holds the view the handler prints through.

        Args:
            view (TournamentView): The view to print through.
        """
        self.view = view

    def render_tournaments(self, tournaments: list[Tournament]) -> None:
        """Prints every tournament, with its dates and its place.

        Args:
            tournaments (list[Tournament]): The tournaments to print.
        """
        self.view.skip_line()
        self.view.console.print(ColorHelper.title("Tournament list"))

        for tournament in tournaments:
            tournament_display = (
                ColorHelper.value(tournament.name)
                + Formatter.label_value("Starts", tournament.start_date)
                + Formatter.label_value("Ends", tournament.end_date)
                + Formatter.label_value("Place", tournament.place)
            )
            self.view.console.print(tournament_display)
        self.view.skip_line()

    def render_selected_tournament_name(self, tournament: Tournament) -> None:
        """Prints the name of the tournament the user is working on.

        Args:
            tournament (Tournament): The selected tournament.
        """
        self.view.skip_line()
        self.view.console.print(
            ColorHelper.title(f"Selected tournament : {tournament.name}")
        )
        self.view.skip_line()

    def render_standings(self, standings: list[TournamentPlayerScore]) -> None:
        """Prints the players and their total, best first.

        Args:
            standings (list[TournamentPlayerScore]): The totals to print.
        """
        self.view.skip_line()
        self.view.console.print(ColorHelper.title("Tournament standings"))
        self.view.skip_line()

        for standing in standings:
            player_display = f"{standing.player.last_name} {standing.player.first_name}"
            self.view.console.print(
                TournamentFormatter.standing(
                    str(standing.tournement_score_value), player_display
                )
            )
        self.view.skip_line()

    def render_tournament_details(self, tournament: Tournament) -> None:
        """Prints the fields of a tournament.

        Args:
            tournament (Tournament): The tournament to print.
        """
        self.view.skip_line()
        self.view.console.print(ColorHelper.title("Tournament details"))

        self.view.console.print(
            Formatter.label_value("Tournament Name", tournament.name)
        )
        self.view.console.print(
            Formatter.label_value("Tournament start date", tournament.start_date)
        )
        self.view.console.print(
            Formatter.label_value("Tournament end date", tournament.end_date)
        )
        self.view.console.print(
            Formatter.label_value(
                "Tournament player count", str(tournament.player_count)
            )
        )
        self.view.console.print(
            Formatter.label_value("Tournament round count", tournament.round_count)
        )
        self.view.skip_line()

    def _render_victory_condition(self, round_match: RoundMatch) -> None:
        """Prints a match, the winner first and the loser second.

        The outcome is read back from the scores: equal scores are a draw, and
        the higher score is the winner.

        Args:
            round_match (RoundMatch): The match to print.
        """
        player_a = f"{round_match.player_score_a.player.last_name} {round_match.player_score_a.player.first_name}"
        player_b = f"{round_match.player_score_b.player.last_name} {round_match.player_score_b.player.first_name}"
        score_a = round_match.player_score_a.score_value
        score_b = round_match.player_score_b.score_value

        match_rendering = "Match : "

        if score_a == score_b:
            victory_condition = "Draw"
            result_display = (
                RoundMatchcolor.draw_label(player_a),
                RoundMatchcolor.draw_label(player_b),
            )
        else:
            victory_condition = "Victory "
            _a = (
                RoundMatchcolor.victory(player_a),
                RoundMatchcolor.defeat(player_b),
            )
            _b = (
                RoundMatchcolor.victory(player_b),
                RoundMatchcolor.defeat(player_a),
            )

            result_display: tuple[str, str] = _a if score_a > score_b else _b

        match_rendering = (
            ColorHelper.label(match_rendering + victory_condition + " ")
            + ColorHelper.value(result_display[0])
            + ColorHelper.label(" vs ")
            + ColorHelper.value(result_display[1])
        )
        self.view.console.print(match_rendering)

    def _render_round_details(self, round: Round) -> None:
        """Prints the name and the timestamps of a round.

        Args:
            round (Round): The round to print.
        """
        self.view.skip_line()
        self.view.console.print(Formatter.label_value("Round", round.name))
        self.view.console.print(Formatter.label_value("Started", round.start_timestamp))
        self.view.console.print(Formatter.label_value("Ended", round.end_timestamp))

    def render_tournament_rounds(self, tournament: Tournament) -> None:
        """Prints every round of a tournament, and every match of every round.

        Args:
            tournament (Tournament): The tournament to print the rounds of.
        """
        self.view.skip_line()
        self.view.console.print(ColorHelper.title("Tournament rounds"))

        for round in tournament.rounds:
            self._render_round_details(round)

            for round_match in round.round_matches:
                self._render_victory_condition(round_match)

        self.view.skip_line()

    def render_playing_round(self, round: Round) -> None:
        """Announces the round being played.

        Args:
            round (Round): The round being played.
        """
        self.view.console.print(f"Playing round : {round.name}")
