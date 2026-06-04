from typing import Any, TypeAlias
from pathlib import Path


from core.core_data_repository import (
    DATA_BASE_ROOT,
    CoreDataRepository,
)

from models.player_registration import PlayerRegistration, PlayerRegistrationInputData

PlayerRegistrations: TypeAlias = list[PlayerRegistration]


class PlayerRegistrationRepository(CoreDataRepository):

    def __init__(self) -> None:
        self.data_path = Path(f"{DATA_BASE_ROOT}/tournaments.json")

    def save_new_player_registration(
        self, user_input: PlayerRegistrationInputData
    ) -> None:
        print("it is fucking saved!")
