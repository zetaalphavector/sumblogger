from typing import Callable, Dict, List, Optional, Type

from src.services.text_completion.client import TextCompletionClientConfig
from src.services.text_completion.types import (
    PromptParams,
    TextCompletionServiceRequest,
)


class TextCompletionService:
    def __init__(
        self,
        text_completion_client_config: TextCompletionClientConfig,
    ):
        raise NotImplementedError

    async def execute(
        self, request: TextCompletionServiceRequest
    ) -> Optional[List[PromptParams]]:
        raise NotImplementedError


class TextCompletionServiceFactory:
    registry: Dict[
        str,
        Type[TextCompletionService],
    ] = {}

    def __init_subclass__(cls):
        cls.registry = {}

    @classmethod
    def register(
        cls,
        service_name: str,
    ) -> Callable:
        def text_completion_inner_wrapper(
            wrapped_class: Type[TextCompletionService],
        ) -> Type[TextCompletionService]:
            cls.registry[service_name] = wrapped_class
            return wrapped_class

        return text_completion_inner_wrapper

    @classmethod
    def create(
        cls,
        service_name: str,
        config: TextCompletionClientConfig,
    ) -> TextCompletionService:
        return cls.registry[service_name](config)
