from controllers.handlers.action import ActionPromptHandler
from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer

from view.player_registration import PlayerRegistrationView

from controllers.shortcuts.player_registration import PlayerRegistrationShortcut

from models.player_registration import PlayerRegistration, PlayerRegistrationInputData


class PlayerRegistrationPromptHandler(CorePromptHandler):

    def __init__(self, view: PlayerRegistrationView) -> None:
        self.view = view

        super().__init__(
            action_prompt_handler=ActionPromptHandler[PlayerRegistration](self.view),
            action_shortcuts=PlayerRegistrationShortcut,
        )

    def get_player_registration_input(self):
        return PlayerRegistrationInputData(
            chess_id=self.view.prompt_player_chess_id(),
            tournament_pk=self.view.prompt_tournament_pk(),
        )


class PlayerRegistrationRenderHandler(CoreRenderer):

    def __init__(self, view: PlayerRegistrationView) -> None:
        self.view = view

    def render_player_registrations(
        self, player_registrations: list[PlayerRegistration]
    ):
        self.view.render_models(player_registrations)
