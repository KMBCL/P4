"""Applies the rules governing the tournaments, and computes their standings."""

from __future__ import annotations

from typing import Any, TypeAlias

from core.result import Result

from repository.helpers.pk import make_pk
from repository.repository import Repository
from repository.paths import TOURNAMENT_DIR
from repository.tournament import TournamentJSON

from models.helpers.flat import flat_round_matches, flat_player_scores
from models.tournament import Tournament, TournamentInputData
from models.round import Round
from models.score import TournamentPlayerScore
from models.player import Player


from service.player_registration import PlayerRegistration
from service.round_match import RoundMatchService

Tournaments: TypeAlias = list[Tournament]


class TournamentStandingsService:
    """Ranks the players of a tournament by the scores they accumulated."""

    def _build_tournament_player_scores(
        self, tournament: Tournament
    ) -> dict[str, TournamentPlayerScore]:
        """Opens an empty total for every registered player.

        Args:
            tournament (Tournament): The tournament to read the players of.

        Returns:
            dict[str, TournamentPlayerScore]: The totals, keyed by chess id.
        """
        tournament_player_scores: dict[str, TournamentPlayerScore] = {
            player.chess_id: TournamentPlayerScore(player)
            for player in tournament.registered_players
        }
        return tournament_player_scores

    def _aggregate_tournament_player_scores(
        self, tournament: Tournament
    ) -> dict[str, TournamentPlayerScore]:
        """Sums, for every player, the scores taken from every match played.

        Args:
            tournament (Tournament): The tournament to read the matches of.

        Returns:
            dict[str, TournamentPlayerScore]: The totals, keyed by chess id.
        """
        flatted_round_matches = flat_round_matches(tournament.rounds)
        flatted_player_score = flat_player_scores(flatted_round_matches)
        tournament_player_scores = self._build_tournament_player_scores(tournament)

        for player_score in flatted_player_score:
            tournament_player_scores[player_score.player.chess_id].increment_score(
                player_score.score_value
            )

        return tournament_player_scores

    def _build_player_scores_list(
        self, aggregated_player_scores: dict[str, TournamentPlayerScore]
    ) -> list[TournamentPlayerScore]:
        """Flattens the totals into a list.

        Args:
            aggregated_player_scores (dict[str, TournamentPlayerScore]): The
                totals, keyed by chess id.

        Returns:
            list[TournamentPlayerScore]: The totals, without their keys.
        """
        return [player_score for _, player_score in aggregated_player_scores.items()]

    def _sort_player_scores_list(
        self, player_scores: list[TournamentPlayerScore]
    ) -> list[TournamentPlayerScore]:
        """Ranks the totals from the highest to the lowest.

        Args:
            player_scores (list[TournamentPlayerScore]): The totals to rank.

        Returns:
            list[TournamentPlayerScore]: The ranked totals.
        """
        return sorted(
            player_scores,
            key=lambda player_score: player_score.tournement_score_value,
            reverse=True,
        )

    def _to_players_list(
        self, player_scores: list[TournamentPlayerScore]
    ) -> list[Player]:
        """Gets the player of every total.

        Args:
            player_scores (list[TournamentPlayerScore]): The totals to read.

        Returns:
            list[Player]: The players.
        """
        return [player_score.player for player_score in player_scores]

    def get_tournament_standings(
        self, tournament: Tournament
    ) -> list[TournamentPlayerScore]:
        """Ranks the registered players by the scores they accumulated.

        Args:
            tournament (Tournament): The tournament to rank the players of.

        Returns:
            list[TournamentPlayerScore]: The totals, best first.
        """
        aggregated_player_scores: dict[str, TournamentPlayerScore] = (
            self._aggregate_tournament_player_scores(tournament)
        )
        player_scores: list[TournamentPlayerScore] = self._build_player_scores_list(
            aggregated_player_scores
        )
        sorted_player_scores: list[TournamentPlayerScore] = (
            self._sort_player_scores_list(player_scores)
        )
        return sorted_player_scores

    def get_players_by_standing(self, tournament: Tournament) -> list[Player]:
        """Ranks the registered players by the scores they accumulated.

        Args:
            tournament (Tournament): The tournament to rank the players of.

        Returns:
            list[Player]: The players, best standing first.
        """
        sorted_player_scores = self.get_tournament_standings(tournament)
        players: list[Player] = self._to_players_list(sorted_player_scores)
        return players


class TournamentService:
    """Creates, reads and stores the tournaments, and registers players to them."""

    def __init__(
        self,
        repository: Repository,
        player_registration: PlayerRegistration,
        round_match_service: RoundMatchService,
    ) -> None:
        """Holds the repository and the services the tournaments are rebuilt with.

        Args:
            repository (Repository): The repository to read and write through.
            player_registration (PlayerRegistration): The registration rules.
            round_match_service (RoundMatchService): The service rebuilding the
                matches of a round.
        """
        self.repository = repository
        self.player_registration = player_registration
        self.round_match_service = round_match_service

    def has_begun(self, tournament: Tournament) -> bool:
        """Tells if the tournament has started to be played.

        Args:
            tournament (Tournament): The tournament to read.

        Returns:
            bool: True when at least one round has been paired.
        """
        round_matches = flat_round_matches(tournament.rounds)
        return bool(round_matches)

    def get_raw_tournament_by_pk(self, tournament_pk: str) -> Result:
        """Reads the stored record of a tournament.

        Args:
            tournament_pk (str): The primary key of the tournament.

        Returns:
            Result:
                - A valid result carrying the stored record.
                - An invalid one when no tournament holds that primary key.
        """
        raw_tournaments: list[dict[str, Any]] = self.repository.get_raw_models(
            TOURNAMENT_DIR
        )
        data_by_field_name = self.repository.extract_data_by_field(
            raw_data=raw_tournaments,
            field_value=tournament_pk,
        )
        if data_by_field_name is None:
            return Result.invalid("No data found")

        return Result.valid(data_by_field_name)

    def _load_registered_players_from_payload(self, tournament: Tournament) -> None:
        """Rebuilds the registered players from the chess ids read from storage.

        Args:
            tournament (Tournament): The tournament to rebuild the players of.
        """
        tournament.registered_players = self.player_registration.to_players(
            tournament.registered_player_payload
        )

    def _load_round_matches_from_payload(
        self, registered_players: list[Player], rounds: list[Round]
    ) -> None:
        """Rebuilds the matches from the pairs read from storage.

        Args:
            registered_players (list[Player]): The players the matches oppose.
            rounds (list[Round]): The rounds to rebuild the matches of.
        """
        self.round_match_service.set_round_matches_from_payload(
            registered_players,
            rounds,
        )

    def _load_related_tournament_models(self, tournament: Tournament) -> None:
        """Rebuilds everything a tournament only holds as a payload.

        Args:
            tournament (Tournament): The tournament to complete.
        """
        self._load_registered_players_from_payload(tournament)
        self._load_round_matches_from_payload(
            tournament.registered_players,
            tournament.rounds,
        )

    def _get_tournaments(self) -> Tournaments:
        """Reads every stored tournament, players and matches rebuilt.

        Returns:
            Tournaments: The tournaments.
        """
        tournaments: Tournaments = [
            TournamentJSON.from_json(raw_tournament)
            for raw_tournament in self.repository.get_raw_models(TOURNAMENT_DIR)
        ]

        for tournament in tournaments:
            self._load_related_tournament_models(tournament)

        return tournaments

    def get_tournament_by_pk(self, tournament_pk: str) -> Result:
        """Reads a tournament, players and matches rebuilt.

        Args:
            tournament_pk (str): The primary key of the tournament.

        Returns:
            Result:
                - A valid result carrying the tournament.
                - An invalid one when no tournament holds that primary key.
        """
        raw_tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not raw_tournament_result:
            return raw_tournament_result

        tournament: Tournament = TournamentJSON.from_json(
            raw_tournament_result.get_value()
        )
        self._load_related_tournament_models(tournament)

        return Result.valid(tournament)

    def get_tournament_by_name(self, tournament_name: str) -> Result:
        """Reads the tournaments whose name contains the given one.

        The comparison ignores case, and matches a part of the name.

        Args:
            tournament_name (str): The name, whole or partial, to look for.

        Returns:
            Result:
                - A valid result carrying the matching tournaments.
                - An invalid one when no name matches.
        """
        tournaments = self._get_tournaments()
        similar_tournaments = [
            tournament
            for tournament in tournaments
            if tournament_name.lower() in tournament.name.lower()
        ]
        if not similar_tournaments:
            return Result.invalid(
                reason=f"No tournaments found with {tournament_name} name"
            )

        return Result.valid(value=similar_tournaments)

    def check_players_left(self, tournament: Tournament) -> Result:
        """Reads the players that could still be registered to the tournament.

        Args:
            tournament (Tournament): The tournament to register to.

        Returns:
            Result:
                - A valid result carrying every stored player.
                - An invalid one when no player is left to register.
        """
        return self.player_registration.check_players_left(tournament)

    def register_player_to_tournament(
        self,
        tournament: Tournament,
        player: Player,
    ) -> Result:
        """Registers a player to the tournament, and stores it.

        Args:
            tournament (Tournament): The tournament to register to.
            player (Player): The player to register.

        Returns:
            Result:
                - A valid result carrying the stored tournament.
                - An invalid one when the player is already registered.
        """
        result = self.player_registration.register_player_to_tournament(
            tournament, player
        )
        if not result:
            return result

        raw_tournament = TournamentJSON.to_json(result.get_value())
        self.repository.update_raw_model(TOURNAMENT_DIR, raw_tournament)
        return result

    def get_registered_players(self, tournament_pk: str) -> Result:
        """Reads the players registered to a tournament.

        Args:
            tournament_pk (str): The primary key of the tournament.

        Returns:
            Result:
                - A valid result carrying the registered players.
                - An invalid one when no tournament holds that primary key, or
                  when it has no player registered.
        """
        tournament_result = self.get_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        tournament: Tournament = tournament_result.get_value()
        if not tournament.registered_players:
            return Result.invalid("No registered players found")

        return Result.valid(value=tournament.registered_players)

    def save_tournament(self, tournament: Tournament) -> None:
        """Stores a tournament over the one holding the same primary key.

        Args:
            tournament (Tournament): The tournament to store.
        """
        tournament_json = TournamentJSON.to_json(tournament)
        self.repository.update_raw_model(
            TOURNAMENT_DIR,
            tournament_json,
        )

    def create_tournament(self, user_input: TournamentInputData) -> Result:
        """Creates a tournament, every round opened, and stores it.

        Args:
            user_input (TournamentInputData): The raw fields typed by the user.

        Returns:
            Result: A valid result carrying the stored tournament.
        """
        tournament = Tournament.from_user_input(
            make_pk(self.repository, TOURNAMENT_DIR),
            user_input,
        )
        self.repository.save_new_raw_model(
            TOURNAMENT_DIR,
            TournamentJSON.to_json(tournament),
        )
        return Result.valid(
            tournament, success_message="Successfully saved new tournament!"
        )

    def get_tournaments(self) -> Result:
        """Reads every stored tournament, players and matches rebuilt.

        Returns:
            Result:
                - A valid result carrying the tournaments.
                - An invalid one when no tournament is stored.
        """
        tournaments = self._get_tournaments()
        if not tournaments:
            return Result.invalid("No tournaments found")

        return Result.valid(tournaments)
