from views.registry import ViewRegistry
from views.view_path import ViewPath

from views.builders.main_view import build_main_view
from views.builders.create_player import build_create_player_view
from views.builders.create_tournament import build_create_tournament_view


def build_view_registry():
    registry = ViewRegistry()
    registry.register_view(ViewPath.MAIN_VIEW, build_main_view())
    registry.register_view(ViewPath.CREATE_PLAYER, build_create_player_view())
    registry.register_view(ViewPath.CREATE_TOURNAMENT, build_create_tournament_view())

    return registry
