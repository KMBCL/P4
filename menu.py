from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Result:
    pass


class Action:
    action: str = "Kawabounga"

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        print(f"{self.action} - DONE !!")


DEFAULT_ACTION = Action()


@dataclass(kw_only=True)
class MenuItem:
    title: str
    shortcut: str
    action: Action | None = None
    parent_item: MenuItem | None = None
    child_items: list[MenuItem] = field(default_factory=list["MenuItem"])

    def add_child_item(self, child_item: MenuItem) -> None:
        child_item.parent_item = self
        self.child_items.append(child_item)

    def back_item(self) -> dict[str, MenuItem] | None:
        if self.parent_item is None:
            return None

        return {"BACK": self.parent_item}

    def build_items(self) -> dict[str, MenuItem]:
        nodes: dict[str, MenuItem] = {}

        for node in self.child_items:
            nodes[node.shortcut] = node

        back_item = self.back_item()
        if back_item:
            nodes.update(**back_item)

        return nodes

    def run(self) -> None:
        if self.action is None:
            return None

        self.action.run()


class MenuRenderer:
    root_item: MenuItem
    actual_item: MenuItem

    def __init__(self, root_item: MenuItem):
        self.root_item = root_item
        self.actual_item = root_item

    def display_items(self, items: dict[str, MenuItem]) -> None:
        for shortcut, item in items.items():
            print(f"{shortcut} - {item.title}")

    def run_menu(self) -> None:
        exit = False

        while not exit:
            child_items = self.actual_item.build_items()

            self.display_items(child_items)

            user_choice = input("Sélectionner une action : ").upper()
            selected_item = child_items.get(user_choice, None)

            if selected_item is None:
                print("Please select available choices")
                continue

            if selected_item.child_items:
                self.actual_item = selected_item

            selected_item.run()


ADD_TOURNAMENT = MenuItem(title="Add tournament", shortcut="AT")
TOURNAMENT_DETAILS = MenuItem(title="Tournament details", shortcut="TD")

HANDLE_TOURNAMENT = MenuItem(
    title="Handle tournament",
    shortcut="HT",
)


def build_tournament_menu() -> MenuItem:
    menu = HANDLE_TOURNAMENT
    menu.add_child_item(ADD_TOURNAMENT)
    menu.add_child_item(TOURNAMENT_DETAILS)
    return menu


ROOT_MENU = MenuItem(
    title="Root menu",
    shortcut="MM",
)


def build_root_menu() -> MenuItem:
    root_menu = ROOT_MENU
    root_menu.add_child_item(build_tournament_menu())
    return root_menu


def __main__():
    menu_renderer = MenuRenderer(root_item=build_root_menu())
    menu_renderer.run_menu()


__main__()
