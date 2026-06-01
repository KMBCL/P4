from __future__ import annotations

from views.view import View
from views.view_path import ViewPath

from controllers.choice import Choice, Choices


def build_main_view() -> View:
    create_player_choice = Choice(
        title="Create player", shortcut="CP", view_path=ViewPath.CREATE_PLAYER
    )
    create_tournament_choice = Choice(
        title="Create tournament", shortcut="CT", view_path=ViewPath.CREATE_TOURNAMENT
    )
    choices = Choices(
        [
            create_player_choice,
            create_tournament_choice,
        ]
    )

    view = View(choices=choices)

    return view
