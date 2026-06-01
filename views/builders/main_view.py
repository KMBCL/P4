from __future__ import annotations

from views.view import View
from views.view_path import ViewPath

from controllers.choice import Choice, Choices


def build_main_view() -> View:
    create_player_choice = Choice(
        title="Create player", shortcut="CP", view_path=ViewPath.CREATE_PLAYER
    )
    choices = Choices([create_player_choice])

    view = View(choices=choices)

    return view
