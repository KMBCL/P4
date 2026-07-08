from __future__ import annotations

from dataclasses import dataclass


from core.core_model import Model, ModelInputData


@dataclass
class PlayerInputData(ModelInputData):
    chess_id: str
    last_name: str
    first_name: str
    birthdate: str


@dataclass
class Player(Model[PlayerInputData]):
    pk: str
    chess_id: str
    last_name: str
    first_name: str
    birthdate: str

    @classmethod
    def from_user_input(cls, new_pk: str, user_input: PlayerInputData) -> Player:
        player = cls(
            pk=new_pk,
            chess_id=user_input.chess_id,
            last_name=user_input.last_name,
            first_name=user_input.first_name,
            birthdate=user_input.birthdate,
        )
        return player
