from __future__ import annotations


class MenuState:

    def __init__(self, should_continue: bool) -> None:
        self.should_continue: bool = should_continue

    @classmethod
    def continue_loop(cls) -> MenuState:
        return MenuState(should_continue=True)

    @classmethod
    def break_loop(cls) -> MenuState:
        return MenuState(should_continue=False)

    def __bool__(self):
        return self.should_continue
