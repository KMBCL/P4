from __future__ import annotations

from typing import TYPE_CHECKING, Any
import inspect

from controllers.menu_state import MenuState

if TYPE_CHECKING:

    from core.core_controller import (
        CoreController,
        RepositoryT,
        PromptHandlerT,
        RendererHandlerT,
    )
    from controllers.action_routing import ActionRouting, Action


class ActionRunner:

    def __init__(
        self,
        target_controller: CoreController[
            PromptHandlerT,
            RendererHandlerT,
        ],
        action_routing: ActionRouting,
    ) -> None:
        self.target_controller = target_controller
        self.action_routing = action_routing

    def back(self) -> MenuState:
        return MenuState.break_loop()

    def get_action_from_routing(self, action_shortcut: str) -> Action | None:
        return self.action_routing.get(action_shortcut, None)

    def warn_user_ignored_kwargs(self, action_kwargs: Any) -> None:
        if action_kwargs:
            self.target_controller.renderer_handler.render_ignored_kwargs(
                action_kwargs=action_kwargs
            )

    def try_to_run_with_kwargs(
        self, action_to_run: Action, action_kwargs: Any
    ) -> MenuState | None:
        signature = inspect.signature(action_to_run)
        parameters = signature.parameters
        has_varkwargs = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in parameters.values()
        )
        expects_args = len(parameters) > 1 or has_varkwargs

        if expects_args and action_kwargs:
            return action_to_run(self.target_controller, **action_kwargs)

        self.warn_user_ignored_kwargs(action_kwargs=action_kwargs)
        return action_to_run(self.target_controller)

    def run(self):
        running = MenuState.continue_loop()
        while running:
            action_shortcut, action_kwargs = (
                self.target_controller.prompt_handler.prompt_action()
            )

            action_to_run = self.get_action_from_routing(action_shortcut)

            if action_to_run is None:
                self.target_controller.renderer_handler.render_undefined_action(
                    action_shortcut
                )
                continue

            result: MenuState | None = self.try_to_run_with_kwargs(
                action_to_run=action_to_run,
                action_kwargs=action_kwargs,
            )
            if result is None:
                continue

            running = result
