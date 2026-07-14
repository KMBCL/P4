"""Runs the menu the user navigates the application through."""

from __future__ import annotations

from typing import TYPE_CHECKING
import inspect

from controllers.handlers.menu import MenuPromptHandler, MenuRendererHandler
from controllers.menu_state import MenuState

from menu.session_context import SessionContext
from models.menu import MenuItem, MenuStructure
from menu.constants import MenuCode

from service.menu import MenuService

if TYPE_CHECKING:
    from controllers.registry import Action, ActionRouting


class MenuController:
    """Displays the menu, and runs the action the user selects."""

    menu_structure: MenuStructure
    actual_menu_item: MenuItem
    menu_item_history: list[MenuItem]

    def __init__(
        self,
        prompt_handler: MenuPromptHandler,
        renderer_handler: MenuRendererHandler,
        registry: ActionRouting,
        menu_service: MenuService,
    ) -> None:
        """Holds the handlers, the registry and the menu the loop runs on.

        The user starts at the root of the menu, with no history behind them.

        Args:
            prompt_handler (MenuPromptHandler): The handler to prompt through.
            renderer_handler (MenuRendererHandler): The handler to print through.
            registry (ActionRouting): The action bound to each menu code.
            menu_service (MenuService): The service reading the menu.
        """
        self.renderer_handler = renderer_handler
        self.prompt_handler = prompt_handler
        self.registry = registry
        self.menu_service = menu_service
        self.menu_structure = menu_service.get_menu_structure()
        self.menu_item_history = []
        self.actual_menu_item = self.menu_structure.root_item
        self.context = SessionContext()

    def _needs_context(self, action_to_run: Action) -> bool:
        """Tells whether the action works on the selections of the user.

        An action asks for them by declaring a session_context parameter.

        Args:
            action_to_run (Action): The action to run.

        Returns:
            bool: True when the action declares that parameter.
        """
        signature = inspect.signature(action_to_run)
        parameters = signature.parameters

        return bool(parameters.get("session_context", None))

    def _find_action(self, menu_item: MenuItem) -> Action | None:
        """Reads the action bound to a menu entry.

        Args:
            menu_item (MenuItem): The entry the user selected.

        Returns:
            Action | None: The action, or None when the code is bound to none.
        """
        return self.registry.get(menu_item.code, None)

    def _run_action(
        self,
        menu_item: MenuItem,
        context: SessionContext,
    ) -> MenuState | None:
        """Runs the action bound to a menu entry, if there is one.

        Args:
            menu_item (MenuItem): The entry the user selected.
            context (SessionContext): The selections of the user.

        Returns:
            MenuState | None: The answer of the action, or None when the code is
                bound to none.
        """
        action = self._find_action(menu_item)
        if action is None:
            return None

        if self._needs_context(action):
            return action(session_context=context)

        return action()

    def _handle_back(self) -> None:
        """Goes back to the menu the user came from."""
        self.actual_menu_item = self.menu_item_history[-1]
        self.menu_item_history.pop(-1)

    def _handle_exit(self, menu_item: MenuItem) -> MenuState:
        """Tells whether the entry the user selected leaves the application.

        Args:
            menu_item (MenuItem): The entry the user selected.

        Returns:
            MenuState: The state stopping the loop on the exit entry, and the
                state keeping it running on any other.
        """
        if menu_item.code != MenuCode.EXIT:
            return MenuState.continue_loop()

        return MenuState.break_loop()

    def _has_sub_menus(self, menu_item: MenuItem) -> bool:
        """Tells whether the entry opens a menu of its own.

        Args:
            menu_item (MenuItem): The entry the user selected.

        Returns:
            bool: True when the entry holds sub menus.
        """
        return bool(menu_item.sub_menus)

    def _handle_navigation(self, menu_item: MenuItem) -> None:
        """Moves the user to the menu the selected entry leads to.

        An entry holding no sub menu leaves the user where they are, so that an
        action can be run again without navigating back to it.

        Args:
            menu_item (MenuItem): The entry the user selected.
        """
        if menu_item.code == MenuCode.BACK:
            return self._handle_back()

        if not self._has_sub_menus(menu_item):
            return None

        self.menu_item_history.append(self.actual_menu_item)
        self.actual_menu_item = menu_item

    def _select_menu_item(
        self, user_input: str, menu_items: list[MenuItem]
    ) -> MenuItem:
        """Reads the entry the user selected, from the rank they typed.

        The entries are numbered from one, as they are displayed.

        Args:
            user_input (str): The validated rank typed by the user.
            menu_items (list[MenuItem]): The entries displayed to the user.

        Returns:
            MenuItem: The selected entry.
        """
        menu_item_index = int(user_input) - 1
        selected_menu_item = menu_items[menu_item_index]
        return selected_menu_item

    def get_menu_input(self):
        """Runs the menu, until the user selects the exit entry.

        The entries of the current menu are displayed, the selected one is run,
        and the user is moved to the menu it leads to.
        """
        menu_state = MenuState.continue_loop()

        while menu_state:
            menu_items = self.actual_menu_item.sub_menus
            self.renderer_handler.render_menu_items(menu_items)
            user_input = self.prompt_handler.prompt_menu_key(menu_items)

            selected_menu_item = self._select_menu_item(user_input, menu_items)

            menu_state = self._handle_exit(selected_menu_item)
            if not menu_state:
                continue

            self._run_action(selected_menu_item, self.context)
            self._handle_navigation(selected_menu_item)
