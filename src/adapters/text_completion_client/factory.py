import enum
from typing import Callable, Dict, Tuple, Type

from src.services.text_completion.client import (
    TextCompletionClient,
    TextCompletionClientConfig,
)


class TextCompletionModelType(enum.Enum):
    CHAT = "chat"
    PROMPT = "prompt"
    PROMPT_WITH_LOGITS = "prompt_with_logits"


class TextCompletionProviderName(enum.Enum):
    OPENAI = "openai"


class TextCompletionClientFactory:
    registry: Dict[
        Tuple[TextCompletionProviderName, TextCompletionModelType],
        Type[TextCompletionClient],
    ] = {}

    def __init_subclass__(cls):
        cls.registry = {}

    @classmethod
    def register(
        cls,
        provider_name: TextCompletionProviderName,
        model_type: TextCompletionModelType,
    ) -> Callable:
        def text_completion_inner_wrapper(
            wrapped_class: Type[TextCompletionClient],
        ) -> Type[TextCompletionClient]:
            cls.registry[(provider_name, model_type)] = wrapped_class
            return wrapped_class

        return text_completion_inner_wrapper

    @classmethod
    def create(
        cls,
        provider_name: TextCompletionProviderName,
        model_type: TextCompletionModelType,
        config: TextCompletionClientConfig,
    ) -> TextCompletionClient:
        return cls.registry[(provider_name, model_type)](**config)
