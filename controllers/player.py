from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
from enum import StrEnum
import re

from views.player import PlayerView

from controllers.result import Result
from controllers.validators.chess_id import ChessIDValidator
from controllers.validators.action import ActionValidator
from controllers.validators.date import DateValidator

from controllers.player_shortcuts import PlayerShortcuts

from models.player import Player, PlayerInputData
from repository.player import PlayerRepository


class PromptController:

    def __init__(self, view: PlayerView) -> None:
        self.view = view
        self.action_validator = ActionValidator()
        self.chess_id_validator = ChessIDValidator()
        self.date_validator = DateValidator()

    def prompt_action(self) -> str:
        while True:
            self.view.render_available_actions()
            user_input = self.view.prompt_action()

            user_input_result = self.action_validator.validate_action_input(
                user_input, action_shortcuts=PlayerShortcuts
            )
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.required_reason)
                continue

            return user_input

    def prompt_chess_id(self) -> str:
        while True:
            user_input = self.view.prompt_chess_id()

            user_input_result = self.chess_id_validator.validate_chess_id(user_input)
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.required_reason)
                continue

            return user_input

    def prompt_last_name(self):
        return self.view.prompt_last_name()

    def prompt_first_name(self):
        return self.view.prompt_first_name()

    def prompt_birthdate(self) -> str:
        while True:
            user_input = self.view.prompt_birthdate()

            user_input_result = self.date_validator.validate_date(user_input)
            if not user_input_result:
                self.view.render_invalid_input(user_input_result.required_reason)
                continue

            return user_input


class RenderController:

    def __init__(self, view: PlayerView) -> None:
        self.view = view

    def render_players(self, players: list[Player]):
        self.view.render_models(players)


class PlayerController:

    def __init__(self, view: PlayerView) -> None:
        self.repository = PlayerRepository()
        self.prompt_controller = PromptController(view=view)
        self.render_controller = RenderController(view=view)

    def build_new_player(self, player_input: PlayerInputData, new_pk: int):
        new_player = Player.from_player_input(new_pk=new_pk, player_input=player_input)
        return new_player

    def get_player_input(self) -> PlayerInputData:
        return PlayerInputData(
            chess_id=self.prompt_controller.prompt_chess_id(),
            last_name=self.prompt_controller.prompt_last_name(),
            first_name=self.prompt_controller.prompt_first_name(),
            birthdate=self.prompt_controller.prompt_birthdate(),
        )

    def create_new_player(self) -> str:

        player = self.build_new_player(
            player_input=self.get_player_input(),
            new_pk=self.repository.make_new_pk(),
        )
        self.repository.write_data(json_data=player.to_json())
        return "success!"

    def show_players(self):
        players = self.repository.get_players()
        self.render_controller.render_players(players)

    def run(self):
        running = True
        while running:
            action = self.prompt_controller.prompt_action()
            if action == PlayerShortcuts.CREATE_PLAYER:
                self.create_new_player()
                continue

            if action == PlayerShortcuts.PLAYERS:
                self.show_players()
                continue
