from views.tournament import TournamentView

from controllers.shortcuts.tournament import TournamentShortcut

from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer

from controllers.handlers.date_prompt import DatePromptHandler
from controllers.handlers.action_prompt import ActionPromptHandler

from models.tournament import Tournament


class TournamentPromptHandler(CorePromptHandler):

    def __init__(self, view: TournamentView) -> None:
        self.view = view
        self.date_prompt_handler = DatePromptHandler[Tournament](self.view)

        super().__init__(
            action_prompt_handler=ActionPromptHandler[Tournament](self.view),
            action_shortcuts=TournamentShortcut,
        )

    def prompt_name(self) -> str:
        return self.view.prompt_name()

    def prompt_place(self) -> str:
        return self.view.prompt_place()

    def prompt_description(self) -> str:
        return self.view.prompt_description()

    def prompt_round_count(self) -> str:
        return self.view.prompt_round_count()

    def prompt_start_date(self) -> str:
        return self.date_prompt_handler.prompt_date(self.view.prompt_start_date)

    def prompt_end_date(self) -> str:
        return self.date_prompt_handler.prompt_date(self.view.prompt_end_date)


class TournamentRenderHandler(CoreRenderer):

    def __init__(self, view: TournamentView) -> None:
        self.view = view

    def render_tournaments(self, tournaments: list[Tournament]):
        self.view.render_models(tournaments)
