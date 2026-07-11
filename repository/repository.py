from __future__ import annotations


from typing import Any
from pathlib import Path
import json


class ExtractMixin:

    def to_data_dict(
        self,
        raw_data: list[dict[str, Any]],
        field_name: str,
    ) -> dict[str, dict[str, Any]]:
        data_by_field_name: dict[str, dict[str, Any]] = {
            str(data[field_name]): data for data in raw_data
        }
        return data_by_field_name

    def _to_data_json(self, data_by_dict: dict[str, dict[str, Any]]):
        data_json = [data for _, data in data_by_dict.items()]
        return data_json

    def extract_data_by_field(
        self,
        raw_data: list[dict[str, Any]],
        field_value: str,
        field_name: str = "pk",
    ) -> dict[str, Any] | None:
        data_by_field_name = self.to_data_dict(raw_data=raw_data, field_name=field_name)
        return data_by_field_name.get(field_value, None)


class Repository(ExtractMixin):

    def _ensure_data_file(self, data_path: Path) -> None:
        if data_path.exists():
            return None

        with open(data_path, "w", encoding="utf-8") as file:
            json.dump([], file)

    def _read_json_file(self, data_path: Path) -> list[dict[str, Any]]:
        self._ensure_data_file(data_path)

        with data_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write_json_data(
        self, data_path: Path, json_data: list[dict[str, Any]]
    ) -> None:
        with data_path.open("w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)

    def _add_model_json(
        self, data_path: Path, model_json: dict[str, Any]
    ) -> list[dict[str, Any]]:
        models = self._read_json_file(data_path)
        models.append(model_json)
        return models

    def _update_model_json(
        self, data_path: Path, model_json: dict[str, Any]
    ) -> list[dict[str, Any]]:
        raw_models = self._read_json_file(data_path)
        models_by_pk = self.to_data_dict(raw_data=raw_models, field_name="pk")
        models_by_pk[model_json["pk"]] = model_json
        uploaded_models = self._to_data_json(models_by_pk)
        return uploaded_models

    def update_raw_model(self, data_path: Path, model_json: dict[str, Any]) -> None:
        updated_models = self._update_model_json(data_path, model_json)
        self._write_json_data(data_path, updated_models)

    def save_new_raw_model(self, data_path: Path, model_json: dict[str, Any]) -> None:
        models = self._add_model_json(data_path, model_json)
        self._write_json_data(data_path, models)

    def get_raw_models(self, data_path: Path) -> list[dict[str, Any]]:
        return self._read_json_file(data_path)

    def _evaluate_filters(
        self, raw_model: dict[str, Any], filters: dict[str, Any]
    ) -> bool:
        match_all_filter = True
        for filter_name, filter_value in filters.items():
            if str(raw_model.get(filter_name, "")).lower() != str(filter_value).lower():
                match_all_filter = False

            if not match_all_filter:
                return match_all_filter

        return match_all_filter

    def get_filtered_raw_models(
        self,
        data_path: Path,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        raw_models = self.get_raw_models(data_path)
        if not filters:
            return raw_models

        filtered_raw_models: list[dict[str, Any]] = []

        for raw_model in raw_models:
            if not self._evaluate_filters(raw_model, filters):
                continue

            filtered_raw_models.append(raw_model)
        return filtered_raw_models
