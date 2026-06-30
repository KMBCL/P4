from __future__ import annotations

from typing import Any, TypeAlias


from core.core_data_repository import (
    TOURNAMENT_DIR,
    PLAYER_DIR,
    CoreDataRepository,
)
from core.result import Result

from models.helpers.flat import flat_rounds
from models.tournament import Tournament, TournamentInputData

from models.player import Player

Tournaments: TypeAlias = list[Tournament]

REGISTERED_PLAYER_CHESS_IDS = "registered_player_chess_ids"

from service.player_registration import PlayerRegistration


class TournamentService:

    def __init__(self) -> None:

        self.repository = CoreDataRepository[Tournament](Tournament)
        self.repository.data_path = TOURNAMENT_DIR
        self.player_registration = PlayerRegistration()

    def has_begun(self, tournament: Tournament) -> bool:
        round_matches = flat_rounds(tournament.rounds)
        return bool(round_matches)

    def get_raw_tournament_by_pk(self, tournament_pk: str) -> Result:
        raw_tournaments: list[dict[str, Any]] = self.repository.read_json_file()
        tournament_result = self.repository.extract_data_by_field(
            raw_data=raw_tournaments,
            field_value=tournament_pk,
        )
        if not tournament_result:
            return tournament_result

        return tournament_result

    def get_tournament_by_pk(self, tournament_pk: str) -> Result:
        raw_tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not raw_tournament_result:
            return raw_tournament_result

        return Result.valid(
            value=Tournament.from_json(raw_tournament_result.get_value())
        )

    def get_tournament_by_name(self, tournament_name: str) -> Result:
        tournaments = self.repository.get_models()
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
            chess_id, self.repository.read_json_file(path=PLAYER_DIR)
        ):
            return Result.invalid(
                reason=f"Player with this chess ID : {chess_id} doesn't exists in database"
            )

        return Result.valid()

    def register_player_to_tournament(
        self,
        tournament_pk: str,
        chess_id: str,
    ) -> Result:
        chess_id_result = self.check_chess_id_exists(chess_id)
        if not chess_id_result:
            return chess_id_result

        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        raw_tournament = tournament_result.get_value()
        result = self.player_registration.register_player_to_tournament(
            raw_tournament=raw_tournament,
            chess_id=chess_id,
        )
        if not result:
            return result

        self.repository.update_model(result.get_value())
        return result

    def extract_registered_players(
        self,
        registered_chess_ids: list[str],
    ):
        raw_players = self.repository.read_json_file(path=PLAYER_DIR)
        registered_raw_players = self.player_registration.extract_registered_players(
            raw_players=raw_players,
            registered_chess_ids=registered_chess_ids,
        )
        registered_players = self.player_registration.to_players(registered_raw_players)

        return registered_players

    def get_registered_players(self, tournament_pk: str) -> Result:
        tournament_result = self.get_raw_tournament_by_pk(tournament_pk)
        if not tournament_result:
            return tournament_result

        registered_players: list[Player] = []
        tournament = tournament_result.get_value()

        registered_chess_ids: list[str] = tournament[REGISTERED_PLAYER_CHESS_IDS]
        if not registered_chess_ids:
            return Result.valid(value=registered_players)

        registered_players = self.extract_registered_players(
            registered_chess_ids=registered_chess_ids,
        )

        return Result.valid(value=registered_players)

    def save_tournament(self, tournament: Tournament) -> None:
        tournament_json = tournament.to_json()
        uploaded_tournaments = self.repository.update_model_json(tournament_json)
        self.repository.write_json_data(uploaded_tournaments)

    def create_tournament(self, user_input: TournamentInputData) -> Result:
        self.repository.save_new_model(user_input)
        return Result.valid(success_message="Successfully saved new tournament!")

    def get_tournaments(self) -> Result:
        tournaments = self.repository.get_models()
        if not tournaments:
            return Result.invalid("No tournaments found")

        return Result.valid(tournaments)
