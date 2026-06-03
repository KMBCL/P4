from typing import TypeAlias, Callable

from controllers.menu_state import MenuState

Action: TypeAlias = Callable[..., MenuState | None]
ActionRouting: TypeAlias = dict[str, Action]
