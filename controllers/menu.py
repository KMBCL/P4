from __future__ import annotations

from typing import TYPE_CHECKING
import inspect

from controllers.handlers.menu import MenuPromptHandler, MenuRendererHandler
from controllers.menu_state import MenuState

from menu.session_context import SessionContext
from models.menu import MenuItem, MenuStructure
from menu.constants import MenuCode

if TYPE_CHECKING:
    from registry import Action, ActionRouting


class MenuController:
    menu_structure: MenuStructure
    actual_menu_item: MenuItem
    menu_item_history: list[MenuItem]

    def __init__(
        self,
        prompt_handler: MenuPromptHandler,
        renderer_handler: MenuRendererHandler,
        registry: ActionRouting,
        menu_structure: MenuStructure,
    ) -> None:
        self.renderer_handler = renderer_handler
        self.prompt_handler = prompt_handler
        self.regisgry = registry
        self.menu_structure = menu_structure
        self.menu_item_history = []
        self.actual_menu_item = self.menu_structure.root_item
        self.context = SessionContext()

    def needs_context(self, action_to_run: Action) -> bool:
        signature = inspect.signature(action_to_run)
        parameters = signature.parameters

        return bool(parameters.get("session_context", None))

    def find_action(self, menu_item: MenuItem) -> Action | None:
        return self.regisgry.get(menu_item.code, None)

    def run_action(
        self,
        menu_item: MenuItem,
        context: SessionContext,
    ) -> MenuState | None:
        action = self.find_action(menu_item)
        if action is None:
            return None

        if self.needs_context(action):
            return action(session_context=context)

        return action()

    def handle_back(self) -> None:

        self.actual_menu_item = self.menu_item_history[-1]
        self.menu_item_history.pop(-1)

    def handle_exit(self, menu_item: MenuItem) -> MenuState:
        if menu_item.code != MenuCode.EXIT:
            return MenuState.continue_loop()

        return MenuState.break_loop()

    def has_sub_menus(self, menu_item: MenuItem) -> bool:
        return bool(menu_item.sub_menus)

    def handle_navigation(self, menu_item: MenuItem) -> None:
        if menu_item.code == MenuCode.BACK:
            return self.handle_back()

        if not self.has_sub_menus(menu_item):
            return None

        self.menu_item_history.append(self.actual_menu_item)
        self.actual_menu_item = menu_item

    def select_menu_item(self, user_input: str, menu_items: list[MenuItem]) -> MenuItem:
        menu_item_index = int(user_input) - 1
        selected_menu_item = menu_items[menu_item_index]
        return selected_menu_item

    def get_menu_input(self):
        menu_state = MenuState.continue_loop()

        while menu_state:
            menu_items = self.actual_menu_item.sub_menus
            self.renderer_handler.render_menu_items(menu_items)
            user_input = self.prompt_handler.prompt_menu_key(menu_items)

            selected_menu_item = self.select_menu_item(user_input, menu_items)

            menu_state = self.handle_exit(selected_menu_item)
            if not menu_state:
                continue

            self.run_action(selected_menu_item, self.context)
            self.handle_navigation(selected_menu_item)
