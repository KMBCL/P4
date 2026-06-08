from typing import Generic, TypeVar, Any

from core.core_handler import CorePromptHandler
from core.core_renderer import CoreRenderer
from core.core_data_repository import CoreDataRepository

from controllers.application_router import APPLICATION_ROUTER

RepositoryT = TypeVar("RepositoryT", bound=CoreDataRepository[Any])
PromptHandlerT = TypeVar("PromptHandlerT", bound=CorePromptHandler)
RendererHandlerT = TypeVar("RendererHandlerT", bound=CoreRenderer)


class CoreController(Generic[PromptHandlerT, RendererHandlerT]):

    def __init__(
        self,
        prompt_handler: PromptHandlerT,
        renderer_handler: RendererHandlerT,
    ) -> None:
        self.prompt_handler = prompt_handler
        self.renderer_handler = renderer_handler

    @staticmethod
    def run_runner(runner_key: str):
        APPLICATION_ROUTER.redirect_to(runner_key)
