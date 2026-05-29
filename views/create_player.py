from __future__ import annotations

from config.view_constants import BACK_SHORTCUT
from controllers.create_player import CreatePlayerAction
from controllers.choice import Choice, Choices

from repository.data import DataSet, INITIAL_DATA_SET

CHOICES = [
    Choice(title="Create player", shortcut="CP", action=CreatePlayerAction()),
    Choice(title="Go back", shortcut=BACK_SHORTCUT),
]


class View:

    def get_data(self):
        data_set = DataSet(INITIAL_DATA_SET)
        return data_set

    def build_choices(self) -> Choices:
        return Choices(CHOICES)
