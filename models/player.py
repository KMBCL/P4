from dataclasses import dataclass

from datetime import date


@dataclass
class Player:
    pk: int
    chess_id: str
    last_name: str
    first_name: str
    birthdate: date | None = None
