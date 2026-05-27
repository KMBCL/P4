from dataclasses import dataclass


@dataclass
class MenuItem:
    title: str
    shortcut: str
    exit: bool = False

    def run_item(self) -> bool:
        print(f"{self.title} - DONE")
        return self.exit
