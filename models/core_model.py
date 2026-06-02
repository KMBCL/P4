from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar


@dataclass
class Model:
    pass


TModel = TypeVar("TModel", bound=Model)
