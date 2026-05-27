from config.menu_constants import EXIT_SHORCUT

from models.menu_item import MenuItem

HANDLE_TOURNAMENT = MenuItem(title="Handle tournament", shortcut="HT")
ADD_TOURNAMENT = MenuItem(title="Add tournament", shortcut="AT")
TOURNAMENT_DETAILS = MenuItem(title="Tournament details", shortcut="TD")
ADD_PLAYER_TO_TOURNAMENT = MenuItem(title="Add player to tournament", shortcut="PT")


HANDLE_PLAYERS = MenuItem(title="Handle players", shortcut="HP")
ADD_PLAYER = MenuItem(title="Add Player", shortcut="AP")
PLAYERS_DETAILS = MenuItem(title="Player details", shortcut="PD")

RUN_TOURNAMENT = MenuItem(title="Run tournament", shortcut="RT")
SELECT_TOURNAMENT = MenuItem(title="Select tournament", shortcut="ST")
RUN_TOURNAMENT_TURN = MenuItem(title="Run tournament turn", shortcut="RT")
ADD_TURN_RESULTS = MenuItem(title="Add turn results", shortcut="AR")

REPORTING = MenuItem(title="Reporting", shortcut="R")
PLAYERS_REPORT = MenuItem(title="Players report", shortcut="PR")
TOURNAMENT_REPORT = MenuItem(title="Tournaments report", shortcut="TR")

EXIT_ITEM = MenuItem(title="EXIT", shortcut=EXIT_SHORCUT)

ROOT_MENU = MenuItem(title="Root menu", shortcut="MM")


def build_tournament_menu() -> MenuItem:
    menu = HANDLE_TOURNAMENT

    ADD_PLAYER_TO_TOURNAMENT.add_child_item(ADD_PLAYER)
    TOURNAMENT_DETAILS.add_child_item(ADD_PLAYER_TO_TOURNAMENT)

    menu.add_child_item(ADD_TOURNAMENT)
    menu.add_child_item(TOURNAMENT_DETAILS)
    return menu


def build_players_menu() -> MenuItem:
    menu = HANDLE_PLAYERS

    menu.add_child_item(ADD_PLAYER)
    menu.add_child_item(PLAYERS_DETAILS)
    return menu


def build_run_tournaments_menu() -> MenuItem:
    menu = RUN_TOURNAMENT

    SELECT_TOURNAMENT.add_child_item(RUN_TOURNAMENT_TURN)
    SELECT_TOURNAMENT.add_child_item(ADD_TURN_RESULTS)

    menu.add_child_item(SELECT_TOURNAMENT)
    return menu


def build_root_menu() -> MenuItem:
    root_menu = ROOT_MENU
    root_menu.add_child_item(build_players_menu())
    root_menu.add_child_item(build_tournament_menu())
    root_menu.add_child_item(build_run_tournaments_menu())
    root_menu.add_child_item(EXIT_ITEM)
    return root_menu
