from core.core_renderer import CoreRenderer
from core.core_handler import CorePromptHandler


from view.round import RoundView


class RoundPromptHandler(CorePromptHandler[RoundView]):

    pass


class RoundRenderHandler(CoreRenderer):

    def __init__(self, view: RoundView) -> None:
        self.view = view
