"""Builds the menu entries a domain object is selected through."""

from models.menu import MenuItem
from models.tournament import Tournament
from models.round import RoundMatch
from models.player import Player


class ModelToMenuItem:
    """Turns domain objects into the menu entries the user picks from."""

    @staticmethod
    def tournament_to_menu_item(tournaments: list[Tournament]) -> list[MenuItem]:
        """Builds one entry per tournament.

        The entries carry no value: the caller reads the tournament back from
        the rank of the entry the user picked.

        Args:
            tournaments (list[Tournament]): The tournaments to pick from.

        Returns:
            list[MenuItem]: The entries, in the order the tournaments are given.
        """
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
        """Builds one entry per player.

        The entries carry no value: the caller reads the player back from the
        rank of the entry the user picked.

        Args:
            players (list[Player]): The players to pick from.

        Returns:
            list[MenuItem]: The entries, in the order the players are given.
        """
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
        """Builds the three outcomes a match can be given.

        Each entry carries the winner it stands for, as its value. The draw
        entry carries none, which is how a draw is told apart from a victory.

        Args:
            round_match (RoundMatch): The match to give an outcome to.

        Returns:
            list[MenuItem]: The entry of player a, of player b, then the draw.
        """
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
