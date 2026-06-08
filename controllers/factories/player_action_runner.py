from rich.console import Console


from view.player import PlayerView
from service.player import PlayerService

from controllers.handlers.player import PlayerPromptHandler, PlayerRenderHandler
from controllers.player import PlayerController


from controllers.shortcuts.player import PlayerShortcut
from controllers.action_routing import ActionRouting
from controllers.action_runner import ActionRunner
from controllers.menu_state import MenuState

ACTION_ROUTING: ActionRouting = {
    PlayerShortcut.CREATE_PLAYER.value.shortcut: PlayerController.create_new_player,
    PlayerShortcut.PLAYERS.value.shortcut: PlayerController.show_players,
    PlayerShortcut.SELECT_PLAYER.value.shortcut: PlayerController.show_player,
    PlayerShortcut.FILTER_PLAYER.value.shortcut: PlayerController.show_filtered_players,
    PlayerShortcut.BACK.value.shortcut: lambda *args, **kwargs: MenuState.break_loop(),
}


def build_player_controller(console: Console) -> PlayerController:
    view = PlayerView(console=console)
    prompt_handler = PlayerPromptHandler(view=view)
    renderer_handler = PlayerRenderHandler(view=view)
    player_controller = PlayerController(
        prompt_handler=prompt_handler,
        renderer_handler=renderer_handler,
    )

    return player_controller


def build_player_action_runner(console: Console) -> ActionRunner:
    player_controller = build_player_controller(console=console)
    action_runner = ActionRunner(
        target_controller=player_controller,
        action_routing=ACTION_ROUTING,
    )

    return action_runner
