from rich.console import Console
from core.core_view import ListView

from view.tournament import TournamentView
from view.player import PlayerView
from view.round import RoundView

console = Console()
list_view = ListView(console)

tournament_view = TournamentView(console)
player_view = PlayerView(console)
round_view = RoundView(console)
