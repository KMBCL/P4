"""Maps a player registered to a tournament to its stored reference."""

from models.player import Player


class PlayerRegistrationJSON:
    """Stores a registered player by reference, rather than by value."""

    @staticmethod
    def to_json(player: Player) -> str:
        """Builds the reference of a registered player.

        Args:
            player (Player): The registered player.

        Returns:
            str: The chess id of the player.
        """
        return player.chess_id
