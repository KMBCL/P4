from views.view import View, ViewDefinition

ADD_PLAYER = ViewDefinition(title="Add Player", shortcut="AP")
PLAYERS_DETAILS = ViewDefinition(title="Player details", shortcut="PD")
HANDLE_PLAYERS = ViewDefinition(title="Handle players", shortcut="HP")

ADD_TURN_RESULTS = ViewDefinition(title="Add turn results", shortcut="AR")
RUN_TOURNAMENT_TURN = ViewDefinition(title="Run tournament turn", shortcut="RT")
SELECT_TOURNAMENT = ViewDefinition(title="Select tournament", shortcut="ST")
RUN_TOURNAMENT = ViewDefinition(title="Run tournament", shortcut="RT")


ADD_TOURNAMENT = ViewDefinition(title="Add tournament", shortcut="AT")
ADD_PLAYER_TO_TOURNAMENT = ViewDefinition(
    title="Add player to tournament", shortcut="PT"
)
TOURNAMENT_DETAILS = ViewDefinition(title="Tournament details", shortcut="TD")

HANDLE_TOURNAMENT = ViewDefinition(title="Handle tournament", shortcut="HT")

EXIT_VIEW = ViewDefinition(title="Exit", shortcut="E")

MAIN_VIEW = ViewDefinition(title="Main view", shortcut="MV")


def build_view(
    root_definition: ViewDefinition,
    child_definitions: list[ViewDefinition] | None = None,
) -> View:
    root_view = View(title=root_definition.title, shortcut=root_definition.shortcut)
    if child_definitions is None:
        return root_view

    root_view.add_child_definitions(child_definitions=child_definitions)

    return root_view


def build_handler_players_view() -> View:
    root_view = build_view(HANDLE_PLAYERS, [ADD_PLAYER, PLAYERS_DETAILS])

    return root_view


def build_handle_tournaments_view() -> View:
    root_view = build_view(HANDLE_TOURNAMENT, [ADD_TOURNAMENT])

    add_player_tournament_view = build_view(ADD_PLAYER_TO_TOURNAMENT, [ADD_PLAYER])
    root_view.add_child_views(child_views=[add_player_tournament_view])

    return root_view


def build_run_tournament_view() -> View:
    root_view = build_view(RUN_TOURNAMENT)

    select_tournament_view = build_view(
        SELECT_TOURNAMENT, [ADD_TURN_RESULTS, RUN_TOURNAMENT_TURN]
    )
    root_view.add_child_views([select_tournament_view])

    return root_view


def build_main_view():
    root_view = build_view(MAIN_VIEW, [EXIT_VIEW])

    root_view.add_child_views(
        [
            build_handler_players_view(),
            build_handle_tournaments_view(),
            build_run_tournament_view(),
        ]
    )

    return root_view
