from __future__ import annotations


from config.view_constants import BACK_SHORTCUT

from views.view import View
from views.view_path import ViewPath

from controllers.create_tournament import CreatePTournamentAction
from controllers.choice import Choice, Choices

from repository.tournament import TournamentRepository


def build_create_tournament_choice(repository: TournamentRepository):
    return Choice(
        title="Create tournament",
        shortcut="CT",
        action=CreatePTournamentAction(repository=repository),
    )


def build_back_to_main_menu():
    return Choice(
        title="Go back",
        shortcut=BACK_SHORTCUT,
        view_path=ViewPath.MAIN_VIEW,
    )


def build_create_tournament_view() -> View:
    repository = TournamentRepository()

    create_tournament = build_create_tournament_choice(repository=repository)
    go_back = build_back_to_main_menu()

    choices = Choices(
        [
            create_tournament,
            go_back,
        ]
    )

    view = View(choices=choices, repository=repository)
    return view
