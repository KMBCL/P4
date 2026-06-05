from typing import Any, TypeAlias
from pathlib import Path


from core.core_data_repository import (
    DATA_BASE_ROOT,
    CoreDataRepository,
)
from models.player import Player

Players: TypeAlias = list[Player]


class PlayerRepository(CoreDataRepository[Player]):

    def __init__(self) -> None:
        super().__init__(model_class=Player)
        self.data_path = Path(f"{DATA_BASE_ROOT}/players.json")
