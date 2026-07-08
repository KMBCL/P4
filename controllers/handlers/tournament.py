from core.color import ColorHelper, RoundMatchcolor, Formatter, TournamentFormatter
from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler

from view.tournament import TournamentView
from controllers.validators.date import DateValidator

from models.tournament import Tournament, TournamentInputData
from models.round import Round, RoundMatch
from models.score import TournamentPlayerScore


class TournamentPromptHandler(CorePromptHandler[TournamentView]):

    def get_tournament_input(self):
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
        return self.view.prompt_register_player()

    def prompt_name(self) -> str:
        return self.view.prompt_name()

    def prompt_place(self) -> str:
        return self.view.prompt_place()

    def prompt_description(self) -> str:
        return self.view.prompt_description()

    def prompt_round_count(self) -> str:
        return self.view.prompt_round_count()

    def prompt_start_date(self) -> str:
        return self.prompt(self.view.prompt_start_date, DateValidator.validate_date)

    def prompt_end_date(self) -> str:
        return self.prompt(self.view.prompt_end_date, DateValidator.validate_date)


class TournamentRenderHandler(CoreRenderer):

    def __init__(self, view: TournamentView) -> None:
        self.view = view

    def render_tournaments(self, tournaments: list[Tournament]) -> None:
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
        self.view.skip_line()
        self.view.console.print(
            ColorHelper.title(f"Selected tournament : {tournament.name}")
        )
        self.view.skip_line()

    def render_standings(self, standings: list[TournamentPlayerScore]) -> None:
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
        self.view.skip_line()
        self.view.console.print(Formatter.label_value("Round", round.name))
        self.view.console.print(Formatter.label_value("Started", round.start_timestamp))
        self.view.console.print(Formatter.label_value("Ended", round.end_timestamp))

    def render_tournament_rounds(self, tournament: Tournament) -> None:
        self.view.skip_line()
        self.view.console.print(ColorHelper.title("Tournament rounds"))

        for round in tournament.rounds:
            self._render_round_details(round)

            for round_match in round.round_matches:
                self._render_victory_condition(round_match)

        self.view.skip_line()
