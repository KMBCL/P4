from views.registry import VIEW_REGISTRY
from views.view_path import ViewPath

from views.builders.main_view import build_main_view
from views.builders.create_player import build_create_player_view

VIEW_REGISTRY.register_view(ViewPath.MAIN_VIEW, build_main_view())
VIEW_REGISTRY.register_view(ViewPath.CREATE_PLAYER, build_create_player_view())
