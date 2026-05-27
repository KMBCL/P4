from dataclasses import dataclass


@dataclass
class Result:
    pass


class Action:
    action: str = "Kawabounga"

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        print(f"{self.action} - DONE !!")


DEFAULT_ACTION = Action()
