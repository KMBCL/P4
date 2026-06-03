from __future__ import annotations

from typing import TYPE_CHECKING, Any


from controllers.menu_state import MenuState

if TYPE_CHECKING:
    from core.core_handler import CorePromptHandler
    from core.core_renderer import CoreRenderer

    from controllers.action_routing import ActionRouting, Action


class ActionRunner:

    def __init__(
        self,
        target_controller: Any,
        action_routing: ActionRouting,
        prompt_handler: CorePromptHandler,
        render_controller: CoreRenderer,
    ) -> None:
        self.target_controller = target_controller
        self.action_routing = action_routing
        self.prompt_handler = prompt_handler
        self.render_controller = render_controller

    def back(self) -> MenuState:
        return MenuState.break_loop()

    def get_action_from_routing(self, action_shortcut: str) -> Action | None:
        return self.action_routing.get(action_shortcut, None)

    def run(self):
        running = MenuState.continue_loop()
        while running:
            action_shortcut, action_kwargs = self.prompt_handler.prompt_action()

            action_to_run = self.get_action_from_routing(action_shortcut)

            if action_to_run is None:
                self.render_controller.render_undefined_action(action_shortcut)
                continue

            result: MenuState | None = action_to_run(
                self.target_controller, **action_kwargs
            )
            if result is None:
                continue

            running = result
