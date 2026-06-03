from typing import TypeAlias, Callable, Any

from controllers.menu_state import MenuState

Action: TypeAlias = Callable[[Any], MenuState | None]
ActionRouting: TypeAlias = dict[str, Action]
