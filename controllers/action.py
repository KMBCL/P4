from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.renderer import Renderer
    from repository.data import DataRepository


class Action:

    def run(
        self,
        fake_repository: DataRepository,
        renderer: Renderer,
    ) -> None: ...
