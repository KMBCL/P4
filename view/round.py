from core.core_view import CoreView
from models.round import Round


class RoundView(CoreView[Round]):

    def prompt_start_datetime(self):
        return self.prompt("Start datetime - YYYY-MM-DD HH:MM")

    def prompt_end_timestamp(self):
        return self.prompt("End datetime - YYYY-MM-DD HH:MM")
