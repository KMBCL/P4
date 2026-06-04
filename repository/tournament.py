from typing import Any, TypeAlias
from pathlib import Path


from core.core_data_repository import (
    DATA_BASE_ROOT,
    DataSet,
    DataItem,
    CoreDataRepository,
)
from models.tournament import Tournament, TournamentInputData

Tournaments: TypeAlias = list[Tournament]


class TournamentRepository(CoreDataRepository):

    def __init__(self) -> None:
        self.data_path = Path(f"{DATA_BASE_ROOT}/tournaments.json")

    def convert_to_model(self, raw_data: list[dict[str, Any]]) -> Tournaments:
        models: Tournaments = []

        for model_data in raw_data:
            model = Tournament.from_json(model_data)
            models.append(model)

        return models

    def get_models(self) -> Tournaments:
        raw_data = self.read_json_file()
        models = self.convert_to_model(raw_data)
        return models

    def get_model(self, key: str, value: str) -> Tournament | None:
        models: Tournaments = self.get_models()

        for model in models:
            attr = getattr(model, key)
            if attr is None:
                continue

            if str(attr) == value:
                return model

        return None

    def save_new_tournament(self, user_input: TournamentInputData) -> None:
        tournament = Tournament.from_user_input(
            new_pk=self.make_new_pk(),
            user_input=user_input,
        )
        self.write_data(json_data=tournament.to_json())
