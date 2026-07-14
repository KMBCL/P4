"""Provides the selections the user carries from one menu action to the next."""

from dataclasses import dataclass


@dataclass
class SessionContext:
    """Holds the tournament and the player the user is currently working on."""

    tournament_pk: str | None = None
    player_pk: str | None = None

    @property
    def required_tournament_pk(self) -> str:
        """Reads the tournament the user selected.

        Returns:
            str: The primary key of the selected tournament.

        Raises:
            ValueError: When no tournament has been selected yet.
        """
        if self.tournament_pk is None:
            raise ValueError("Undefined tournament pk")

        return self.tournament_pk
