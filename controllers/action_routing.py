from typing import TypeAlias, Callable, Any

ActionRouting: TypeAlias = dict[str, Callable[[Any], None]]
