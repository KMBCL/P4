"""Provides the base every domain model is built on."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, Any, Self, Generic


@dataclass
class ModelInputData:
    """Carries the raw fields of a model, as they were typed by the user."""

    pass


TModelInputData = TypeVar("TModelInputData", bound=ModelInputData)


@dataclass
class Model(Generic[TModelInputData]):
    """Bases a domain model, built from the input data of its own type."""

    @classmethod
    def from_user_input(cls, new_pk: str, user_input: TModelInputData) -> Self:
        """Builds a model from validated user input.

        Args:
            new_pk (str): The primary key assigned to the new model.
            user_input (TModelInputData): The raw fields typed by the user.

        Returns:
            Self: The new model.
        """
        ...


TModel = TypeVar("TModel", bound=Model[Any])
TModels = list[TModel]
