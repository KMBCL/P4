from dataclasses import dataclass
from pathlib import Path

from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_BASE_ROOT = f"{BASE_DIR}/database"


@dataclass
class DataItem:
    content: str
    shortcut: str


@dataclass
class DataSet:
    data_items: list[DataItem]

    def add_data(self, data_item: DataItem) -> None:
        self.data_items.append(data_item)

    def new_pk(self) -> int:
        return len(self.data_items) + 1


class DataRepository:
    data_path: Path

    def __init__(self) -> None:
        pass

    def get_data(self) -> DataSet: ...

    def write_data(self, json_data: dict[str, Any]): ...
