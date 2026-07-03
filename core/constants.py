from dataclasses import dataclass
from enum import StrEnum

from models.player import Player


class WinningCondition(StrEnum):
    VICTORY = "1"
    DEFEAT = "2"
    DRAW = "3"
