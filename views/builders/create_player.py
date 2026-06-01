from __future__ import annotations


from config.view_constants import BACK_SHORTCUT

from views.view import View
from views.view_path import ViewPath

from controllers.create_player import CreatePlayerAction
from controllers.choice import Choice, Choices

from repository.player_repository import PlayerRepository


def build_create_player_choice(repository: PlayerRepository):
    return Choice(
        title="Create player",
        shortcut="CP",
        action=CreatePlayerAction(repository=repository),
    )


def build_back_to_main_menu():
    return Choice(
        title="Go back",
        shortcut=BACK_SHORTCUT,
        view_path=ViewPath.MAIN_VIEW,
    )


def build_create_player_view() -> View:
    repository = PlayerRepository()

    create_player = build_create_player_choice(repository=repository)
    go_back = build_back_to_main_menu()

    choices = Choices(
        [
            create_player,
            go_back,
        ]
    )

    view = View(choices=choices, repository=repository)
    return view
