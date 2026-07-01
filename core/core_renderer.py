from typing import Any

from view.core_view import CoreView


class CoreRenderer:

    def __init__(self, view: CoreView[Any]) -> None:
        self.view = view
