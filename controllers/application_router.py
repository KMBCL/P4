from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.action_runner import ActionRunner


class ApplicationRouter:

    def __init__(self) -> None:
        self.action_runners: dict[str, ActionRunner] = {}

    def register(self, name: str, action_runner: ActionRunner) -> None:
        self.action_runners[name] = action_runner

    def redirect_to(self, target_name: str) -> None:
        if target_name not in self.action_runners:
            raise ValueError("Fuck off")

        self.action_runners[target_name].run()


APPLICATION_ROUTER = ApplicationRouter()
