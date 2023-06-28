import enum
import json
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

    clients: Dict[
        Tuple[
            TextCompletionProviderName,
            TextCompletionModelType,
            str,
        ],
        TextCompletionClient,
    ] = {}

    def __init_subclass__(cls):
        cls.registry = {}
        cls.clients = {}

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
    def __hashed(cls, config: TextCompletionClientConfig):
        return json.dumps(config, sort_keys=True)

    @classmethod
    def create(
        cls,
        provider_name: TextCompletionProviderName,
        model_type: TextCompletionModelType,
        config: TextCompletionClientConfig,
    ) -> TextCompletionClient:
        if (provider_name, model_type, cls.__hashed(config)) not in cls.clients:
            client = cls.registry[(provider_name, model_type)](**config)
            cls.clients[(provider_name, model_type, cls.__hashed(config))] = client
        else:
            client = cls.clients[(provider_name, model_type, cls.__hashed(config))]

        return client
