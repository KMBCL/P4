from menu_item import MenuItem

HANDLE_TOURNAMENTS = MenuItem("Handle tournaments", "HT")
HANDLE_PLAYERS = MenuItem("Handle players", "HP")
RUN_TOURNAMENT = MenuItem("Run tournament", "RT")
REPORTING = MenuItem("Reporting", "R")
EXIT_ITEM = MenuItem("Exit", "E", exit=True)

MAIN_MENU = [
    HANDLE_TOURNAMENTS,
    HANDLE_PLAYERS,
    RUN_TOURNAMENT,
    REPORTING,
    EXIT_ITEM,
]

ADD_TOURNAMENT = MenuItem("Add tournament", "AT")
TOURNAMENT_DETAILS = MenuItem("Tournament details", "TD")

TOURNAMENT_MENU = [
    ADD_TOURNAMENT,
    TOURNAMENT_DETAILS,
]
