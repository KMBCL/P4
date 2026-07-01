from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Type
from pathlib import Path
import json

from typing import Any

from core.core_model import TModel, ModelInputData
from core.result import Result

BASE_DIR = Path(__file__).resolve().parent
DATA_BASE_ROOT = f"{BASE_DIR.parent}/database"

PLAYER_DIR = Path(f"{DATA_BASE_ROOT}/players.json")
TOURNAMENT_DIR = Path(f"{DATA_BASE_ROOT}/tournaments.json")
MENU_DIR = Path(f"{DATA_BASE_ROOT}/menu.json")
