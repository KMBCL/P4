"""Wraps a value in the Rich markup giving it its colour."""


class MenuColorHelper:
    """Colours a menu entry."""

    @staticmethod
    def action(value: str) -> str:
        """Colours an entry running an action."""
        return f"[bright_blue]{value}[/bright_blue]"

    @staticmethod
    def navigation(value: str) -> str:
        """Colours an entry opening a sub menu."""
        return f"[bright_cyan]{value}[/bright_cyan]"

    @staticmethod
    def back(value: str) -> str:
        """Colours an entry leaving the current menu."""
        return f"[bright_red]{value}[/bright_red]"


class ColorHelper:
    """Colours a value."""

    @staticmethod
    def success(value: str) -> str:
        """Colours a successful outcome."""
        return f"[green]{value}[/green]"

    @staticmethod
    def invalid(value: str) -> str:
        """Colours the reason an input was rejected."""
        return f"[red]{value}[/red]"

    @staticmethod
    def input(value: str) -> str:
        """Colours the prompt awaiting an input."""
        return f"[orange1]{value}[/orange1]"

    @staticmethod
    def title(value: str) -> str:
        """Colours a title."""
        return f"[yellow]{value}[/yellow]"

    @staticmethod
    def value(value: str) -> str:
        """Colours the value of a field."""
        return f"[green]{value}[/green]"

    @staticmethod
    def label(value: str) -> str:
        """Colours the label of a field."""
        return f"[cyan]{value}[/cyan]"


class RoundMatchcolor:
    """Colours the outcome of a match."""

    @staticmethod
    def victory_label(value: str) -> str:
        """Colours the label of a victory."""
        return f"[cyan]{value}[/cyan]"

    @staticmethod
    def draw_label(value: str) -> str:
        """Colours the label of a draw."""
        return f"[dark_orange]{value}[/dark_orange]"

    @staticmethod
    def defeat(value: str) -> str:
        """Colours a defeat."""
        return f"[dark_red]{value}[/dark_red]"

    @staticmethod
    def victory(value: str) -> str:
        """Colours a victory."""
        return f"[green1]{value}[/green1]"


class Formatter:
    """Lays out a field on a single line."""

    @staticmethod
    def label_value(label: str, value: str) -> str:
        """Lays out a field as its label, then its value.

        Args:
            label (str): The name of the field.
            value (str): The value of the field.

        Returns:
            str: The coloured line.
        """
        return f" - {ColorHelper.label(label)} : {ColorHelper.value(value)}"


class TournamentFormatter:
    """Lays out a standing on a single line."""

    @staticmethod
    def standing(score: str, player: str) -> str:
        """Lays out a standing as its score, then its player.

        Args:
            score (str): The score accumulated by the player.
            player (str): The name of the player.

        Returns:
            str: The coloured line.
        """
        return f"{ColorHelper.title(score)} - {ColorHelper.value(player)}"
