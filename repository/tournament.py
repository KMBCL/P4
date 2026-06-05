from typing import Any, TypeAlias
from pathlib import Path


from core.core_data_repository import (
    DATA_BASE_ROOT,
    CoreDataRepository,
)
from models.tournament import Tournament

Tournaments: TypeAlias = list[Tournament]


class TournamentRepository(CoreDataRepository[Tournament]):

    def __init__(self) -> None:
        super().__init__(model_class=Tournament)
        self.data_path = Path(f"{DATA_BASE_ROOT}/tournaments.json")
