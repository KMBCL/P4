from repository.build import repository


from service.tournament import TournamentService, TournamentStandingsService
from service.player import PlayerService
from service.round import RoundService
from service.round_match import RoundMatchService
from service.player_registration import PlayerRegistration
from service.menu import MenuService

player_service = PlayerService(repository)
round_service = RoundService()
round_match_service = RoundMatchService(repository)
player_registration_service = PlayerRegistration(player_service)
tournament_service = TournamentService(
    repository,
    player_registration_service,
    round_match_service,
)
tournament_standing_service = TournamentStandingsService()
menu_service = MenuService(repository)
