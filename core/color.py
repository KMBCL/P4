class ColorHelper:

    @staticmethod
    def title(value: str) -> str:
        return f"[yellow]{value}[/yellow]"

    @staticmethod
    def value(value: str) -> str:
        return f"[green]{value}[/green]"

    @staticmethod
    def label(value: str) -> str:
        return f"[cyan]{value}[/cyan]"


class RoundMatchcolor:
    @staticmethod
    def victory_label(value: str) -> str:
        return f"[cyan]{value}[/cyan]"

    @staticmethod
    def draw_label(value: str) -> str:
        return f"[dark_orange]{value}[/dark_orange]"

    @staticmethod
    def defeat(value: str) -> str:
        return f"[dark_red]{value}[/dark_red]"

    @staticmethod
    def victory(value: str) -> str:
        return f"[green1]{value}[/green1]"


class Formatter:

    @staticmethod
    def label_value(label: str, value: str) -> str:
        return f" - {ColorHelper.label(label)} : {ColorHelper.value(value)}"


class TournamentFormatter:

    @staticmethod
    def standing(score: str, player: str) -> str:
        return f"{ColorHelper.title(score)} - {ColorHelper.value(player)}"
