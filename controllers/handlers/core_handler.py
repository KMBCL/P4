from abc import ABC, abstractmethod


class PromptHandler(ABC):

    @abstractmethod
    def prompt_action(self) -> str: ...
