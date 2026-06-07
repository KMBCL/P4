from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Any, Self, Generic


@dataclass
class ModelInputData:
    pass


TModelInputData = TypeVar("TModelInputData", bound=ModelInputData)


@dataclass
class Model(Generic[TModelInputData]):
    pass

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Self: ...

    def to_json(self) -> dict[str, Any]: ...

    @classmethod
    def from_user_input(cls, new_pk: str, user_input: TModelInputData) -> Self: ...


TModel = TypeVar("TModel", bound=Model[Any])
TModels = list[TModel]
