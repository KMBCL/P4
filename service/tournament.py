from __future__ import annotations

from typing import Any, TypeAlias

from core.result import Result

from repository.helpers.pk import make_pk
from repository.repository import Repository
from repository.paths import TOURNAMENT_DIR, PLAYER_DIR
from repository.tournament import TournamentJSON
from repository.round import RoundJSON, RoundMatchJSON

from models.helpers.flat import flat_round_matches
from models.tournament import Tournament, TournamentInputData
from models.round import Round

from models.player import Player


from service.player_registration import PlayerRegistration
from service.round_match import RoundMatchService

Tournaments: TypeAlias = list[Tournament]


class TournamentService:

    def __init__(
        self,
        repository: Repository,
        player_registration: PlayerRegistration,
        round_match_service: RoundMatchService,
    ) -> None:
        self.repository = repository
        self.player_registration = player_registration
        self.round_match_service = round_match_service

    def has_begun(self, tournament: Tournament) -> bool:
        round_matches = flat_round_matches(tournament.rounds)
        return bool(round_matches)

    def get_raw_tournament_by_pk(self, tournament_pk: str) -> Result:
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
        tournament.registered_players = self.player_registration.to_players(
            tournament.registered_player_payload
        )

    def _load_round_matches_from_payload(
        self, registered_players: list[Player], rounds: list[Round]
    ) -> None:
        self.round_match_service.set_round_matches_from_payload(
            registered_players,
            rounds,
        )

    def _get_tournaments(self) -> Tournaments:
        tournaments: Tournaments = [
            TournamentJSON.from_json(raw_tournament)
            for raw_tournament in self.repository.get_raw_models(TOURNAMENT_DIR)
        ]

        for tournament in tournaments:
            self._load_registered_players_from_payload(tournament)
            self._load_round_matches_from_payload(
                tournament.registered_players,
                tournament.rounds,
            )

        return tournaments

    def get_tournament_by_pk(self, tournament_pk: str) -> Result:
        raw_tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not raw_tournament_result:
            return raw_tournament_result

        tournament: Tournament = TournamentJSON.from_json(
            raw_tournament_result.get_value()
        )
        self._load_registered_players_from_payload(tournament)
        self._load_round_matches_from_payload(
            tournament.registered_players,
            tournament.rounds,
        )

        return Result.valid(tournament)

    def get_tournament_by_name(self, tournament_name: str) -> Result:
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

    def check_chess_id_exists(self, chess_id: str) -> Result:
        if not self.player_registration.validate_chess_id_exists(
            chess_id, self.repository.get_raw_models(PLAYER_DIR)
        ):
            return Result.invalid(
                reason=f"Player with this chess ID : {chess_id} doesn't exists in database"
            )

        return Result.valid()

    def register_player_to_tournament(
        self,
        tournament: Tournament,
        player: Player,
    ) -> Result:
        result = self.player_registration.register_player_to_tournament(
            tournament, player
        )
        if not result:
            return result

        raw_tournament = TournamentJSON.to_json(result.get_value())
        self.repository.update_raw_model(TOURNAMENT_DIR, raw_tournament)
        return result

    def get_registered_players(self, tournament_pk: str) -> Result:
        tournament_result = self.get_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        tournament: Tournament = tournament_result.get_value()
        if not tournament.registered_players:
            return Result.invalid("No registered players found")

        return Result.valid(value=tournament.registered_players)

    def save_tournament(self, tournament: Tournament) -> None:
        tournament_json = TournamentJSON.to_json(tournament)
        self.repository.update_raw_model(
            TOURNAMENT_DIR,
            tournament_json,
        )

    def create_tournament(self, user_input: TournamentInputData) -> Result:
        tournament = Tournament.from_user_input(
            make_pk(self.repository, TOURNAMENT_DIR),
            user_input,
        )
        self.repository.save_new_raw_model(
            TOURNAMENT_DIR,
            TournamentJSON.to_json(tournament),
        )
        return Result.valid(success_message="Successfully saved new tournament!")

    def get_tournaments(self) -> Result:
        tournaments = self._get_tournaments()
        if not tournaments:
            return Result.invalid("No tournaments found")

        return Result.valid(tournaments)
