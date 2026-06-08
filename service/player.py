from typing import Any, TypeAlias
from pathlib import Path


from core.core_data_repository import (
    PLAYER_DIR,
    CoreDataRepository,
)
from models.player import Player

Players: TypeAlias = list[Player]


class PlayerService:

    def __init__(self) -> None:
        self.repository = CoreDataRepository[Player](Player)
        self.repository.data_path = PLAYER_DIR
