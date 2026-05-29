from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from controllers.renderer import Renderer


TRepository = TypeVar("TRepository")


class Action(Generic[TRepository]):

    def __init__(self, repository: TRepository) -> None:
        self.repository = repository

    def run(
        self,
        renderer: Renderer,
    ) -> None: ...
