from abc import ABC, abstractmethod


class PromptHandler(ABC):

    @abstractmethod
    def prompt_action(self) -> tuple[str, dict[str, str]]: ...
