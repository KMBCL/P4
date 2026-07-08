from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Any, Self, Generic


@dataclass
class ModelInputData:
    pass


TModelInputData = TypeVar("TModelInputData", bound=ModelInputData)


@dataclass
class Model(Generic[TModelInputData]):

    @classmethod
    def from_user_input(cls, new_pk: str, user_input: TModelInputData) -> Self: ...


TModel = TypeVar("TModel", bound=Model[Any])
TModels = list[TModel]
