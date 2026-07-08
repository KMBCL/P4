from dataclasses import dataclass


@dataclass
class SessionContext:
    tournament_pk: str | None = None
    player_pk: str | None = None

    @property
    def required_tournament_pk(self) -> str:
        if self.tournament_pk is None:
            raise ValueError("Undefined tournament pk")

        return self.tournament_pk
