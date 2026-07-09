from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler


from view.round import RoundView


class RoundPromptHandler(CorePromptHandler[RoundView]):

    def prompt_start_datetime(self) -> str:
        return self.view.prompt_start_datetime()

    def prompt_end_timestamp(self) -> str:
        return self.view.prompt_end_timestamp()


class RoundRenderHandler(CoreRenderer):

    def __init__(self, view: RoundView) -> None:
        self.view = view
