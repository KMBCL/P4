"""Provides the player domain model."""

from __future__ import annotations

from dataclasses import dataclass


from core.core_model import Model, ModelInputData


@dataclass
class PlayerInputData(ModelInputData):
    """Carries the raw player fields as they were typed by the user."""

    chess_id: str
    last_name: str
    first_name: str
    birthdate: str


@dataclass
class Player(Model[PlayerInputData]):
    """Represents a chess player. chess_id is used across tournaments."""

    pk: str
    chess_id: str
    last_name: str
    first_name: str
    birthdate: str

    @classmethod
    def from_user_input(cls, new_pk: str, user_input: PlayerInputData) -> Player:
        """Builds a player from validated user input.

        Args:
            new_pk (str): The primary key assigned to the new player.
            user_input (PlayerInputData): The raw fields typed by the user.

        Returns:
            Player: The new player.
        """
        player = cls(
            pk=new_pk,
            chess_id=user_input.chess_id,
            last_name=user_input.last_name,
            first_name=user_input.first_name,
            birthdate=user_input.birthdate,
        )
        return player
