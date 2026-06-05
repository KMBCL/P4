from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, Type
from pathlib import Path
import json

from typing import Any

from core.core_model import TModel, Model, ModelInputData

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


class CoreDataRepository(Generic[TModel]):
    data_path: Path

    def __init__(self, model_class: Type[TModel]) -> None:
        self.data_path = Path()
        self.model_class = model_class

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

    def convert_to_model(self, raw_data: list[dict[str, Any]]) -> list[TModel]:
        models: list[TModel] = []

        for model_data in raw_data:
            model = self.model_class.from_json(model_data)
            models.append(model)

        return models

    def get_models(self) -> list[TModel]:
        raw_data = self.read_json_file()
        models = self.convert_to_model(raw_data)
        return models

    def get_model(self, key: str, value: str) -> TModel | None:
        models: list[TModel] = self.get_models()

        for model in models:
            attr = getattr(model, key)
            if attr is None:
                continue

            if str(attr) == value:
                return model

        return None

    def get_filtered_models(self, filters: dict[str, Any]) -> list[TModel]:
        models = self.get_models()
        if not filters:
            return models

        filtered_models: list[TModel] = []

        for model in models:
            match_all_filters = True

            for filter_name, filter_value in filters.items():

                try:
                    model_attr: Any | None = getattr(model, filter_name)

                    if model_attr is None:
                        match_all_filters = False
                        break

                    if str(model_attr).lower() != str(filter_value).lower():
                        match_all_filters = False
                        break

                except AttributeError:
                    match_all_filters = False
                    continue

            if match_all_filters:
                filtered_models.append(model)

        return filtered_models

    def save_new_model(self, user_input: ModelInputData) -> None:
        model = self.model_class.from_user_input(
            new_pk=self.make_new_pk(),
            user_input=user_input,
        )
        self.write_data(json_data=model.to_json())
