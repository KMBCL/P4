from menu.constants import MenuCode

from models.menu import MenuItem
from models.tournament import Tournament
from models.round import RoundMatch
from models.player import Player


class ModelToMenuItem:

    @staticmethod
    def tournament_to_menu_item(tournaments: list[Tournament]) -> list[MenuItem]:
        menu_items: list[MenuItem] = [
            MenuItem(
                code=tournament.pk,
                title=tournament.name,
            )
            for tournament in tournaments
        ]
        return menu_items

    @staticmethod
    def player_to_menu_item(players: list[Player]) -> list[MenuItem]:
        menu_items: list[MenuItem] = [
            MenuItem(
                code=player.chess_id,
                title=f"{player.first_name} - {player.last_name}",
            )
            for player in players
        ]
        return menu_items

    @staticmethod
    def round_match_to_winning_condition_menu_item(
        round_match: RoundMatch,
    ) -> list[MenuItem]:
        player_a = round_match.player_score_a.player
        player_b = round_match.player_score_b.player
        menu_items: list[MenuItem] = [
            MenuItem(
                code=player_a.chess_id,
                title=f"Winner : {player_a.last_name} - {player_a.first_name}",
                value=player_a,
            ),
            MenuItem(
                code=player_b.chess_id,
                title=f"Winner : {player_b.last_name} - {player_b.first_name}",
                value=player_b,
            ),
            MenuItem(code="draw", title="Draw"),
        ]
        return menu_items
