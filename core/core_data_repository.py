from dataclasses import dataclass
from typing import Any
from pathlib import Path
import json

from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_BASE_ROOT = f"{BASE_DIR.parent}/database"


@dataclass
class DataItem:
    content: str
    shortcut: str


@dataclass
class DataSet:
    data_items: list[DataItem]

    def add_data(self, data_item: DataItem) -> None:
        self.data_items.append(data_item)


class CoreDataRepository:
    data_path: Path

    def __init__(self) -> None:
        self.data_path = Path()

    def get_data(self) -> DataSet: ...

    def read_json_file(self) -> list[dict[str, Any]]:
        with self.data_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def write_data(self, json_data: dict[str, Any]):
        models = self.read_json_file()
        models.append(json_data)

        with self.data_path.open("w", encoding="utf-8") as file:
            json.dump(models, file, indent=4, ensure_ascii=False)

    def make_new_pk(self) -> int:
        raw_data = self.read_json_file()
        new_pk = len(raw_data) + 1

        return new_pk
