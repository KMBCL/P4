"""Reads and writes raw records from / to the JSON files."""

from __future__ import annotations


from typing import Any
from pathlib import Path
import json


class ExtractMixin:
    """Indexes raw records by one of their fields."""

    def to_data_dict(
        self,
        raw_data: list[dict[str, Any]],
        field_name: str,
    ) -> dict[str, dict[str, Any]]:
        """Indexes raw records by the value of one field.

        Args:
            raw_data (list[dict[str, Any]]): The records to index.
            field_name (str): The field whose value keys the index.

        Returns:
            dict[str, dict[str, Any]]: The records, keyed by field value.
        """
        data_by_field_name: dict[str, dict[str, Any]] = {
            str(data[field_name]): data for data in raw_data
        }
        return data_by_field_name

    def _to_data_json(self, data_by_dict: dict[str, dict[str, Any]]):
        """Flattens an index back into a list of records.

        Args:
            data_by_dict (dict[str, dict[str, Any]]): The indexed records.

        Returns:
            list[dict[str, Any]]: The records, without their keys.
        """
        data_json = [data for _, data in data_by_dict.items()]
        return data_json

    def extract_data_by_field(
        self,
        raw_data: list[dict[str, Any]],
        field_value: str,
        field_name: str = "pk",
    ) -> dict[str, Any] | None:
        """Finds the single record whose field holds the given value.

        Args:
            raw_data (list[dict[str, Any]]): The records to search.
            field_value (str): The value to look for.
            field_name (str): The field to look into. Defaults to the primary key.

        Returns:
            dict[str, Any] | None: The matching record, or None when there is none.
        """
        data_by_field_name = self.to_data_dict(raw_data=raw_data, field_name=field_name)
        return data_by_field_name.get(field_value, None)


class Repository(ExtractMixin):
    """Stores raw records in a JSON file, given as an argument to every call."""

    def _ensure_data_file(self, data_path: Path) -> None:
        """Creates the file, holding no record, when it does not exist yet.

        Args:
            data_path (Path): The JSON file to create.
        """
        if data_path.exists():
            return None

        with open(data_path, "w", encoding="utf-8") as file:
            json.dump([], file)

    def _read_json_file(self, data_path: Path) -> list[dict[str, Any]]:
        """Reads every record of the file.

        Args:
            data_path (Path): The JSON file to read.

        Returns:
            list[dict[str, Any]]: The stored records.
        """
        self._ensure_data_file(data_path)

        with data_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write_json_data(
        self, data_path: Path, json_data: list[dict[str, Any]]
    ) -> None:
        """Writes the records to the file, replacing the ones already there.

        Args:
            data_path (Path): The JSON file to write.
            json_data (list[dict[str, Any]]): The records to store.
        """
        with data_path.open("w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)

    def _add_model_json(
        self, data_path: Path, model_json: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Appends a record to the ones already stored.

        Args:
            data_path (Path): The JSON file to read.
            model_json (dict[str, Any]): The record to append.

        Returns:
            list[dict[str, Any]]: The stored records, and the new one.
        """
        models = self._read_json_file(data_path)
        models.append(model_json)
        return models

    def _update_model_json(
        self, data_path: Path, model_json: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Replaces the stored record holding the same primary key.

        Args:
            data_path (Path): The JSON file to read.
            model_json (dict[str, Any]): The record to replace.

        Returns:
            list[dict[str, Any]]: The stored records, with the given one replaced.
        """
        raw_models = self._read_json_file(data_path)
        models_by_pk = self.to_data_dict(raw_data=raw_models, field_name="pk")
        models_by_pk[model_json["pk"]] = model_json
        updated_models = self._to_data_json(models_by_pk)
        return updated_models

    def update_raw_model(self, data_path: Path, model_json: dict[str, Any]) -> None:
        """Stores a record over the one holding the same primary key.

        Args:
            data_path (Path): The JSON file to write.
            model_json (dict[str, Any]): The record to store.
        """
        updated_models = self._update_model_json(data_path, model_json)
        self._write_json_data(data_path, updated_models)

    def save_new_raw_model(self, data_path: Path, model_json: dict[str, Any]) -> None:
        """Stores a record that was never stored before.

        Args:
            data_path (Path): The JSON file to write.
            model_json (dict[str, Any]): The record to store.
        """
        models = self._add_model_json(data_path, model_json)
        self._write_json_data(data_path, models)

    def get_raw_models(self, data_path: Path) -> list[dict[str, Any]]:
        """Reads every record of the file.

        Args:
            data_path (Path): The JSON file to read.

        Returns:
            list[dict[str, Any]]: The stored records.
        """
        return self._read_json_file(data_path)

    def _evaluate_filters(
        self, raw_model: dict[str, Any], filters: dict[str, Any]
    ) -> bool:
        """Tells whether a record matches every filter.

        Fields and values are compared as strings.

        Args:
            raw_model (dict[str, Any]): The record to evaluate.
            filters (dict[str, Any]): The awaited value of each filtered field.

        Returns:
            bool: True when every filter matches.
        """
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
        """Reads the records matching every filter.

        Args:
            data_path (Path): The JSON file to read.
            filters (dict[str, Any]): The awaited value of each filtered field.
                Empty filters keep every record.

        Returns:
            list[dict[str, Any]]: The matching records.
        """
        raw_models = self.get_raw_models(data_path)
        if not filters:
            return raw_models

        filtered_raw_models: list[dict[str, Any]] = []

        for raw_model in raw_models:
            if not self._evaluate_filters(raw_model, filters):
                continue

            filtered_raw_models.append(raw_model)
        return filtered_raw_models
