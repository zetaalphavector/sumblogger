from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar

from typing_extensions import TypedDict, Unpack

from src.services.text_completion.types import LLMConfig


class TextCompletionRequest(TypedDict):
    llm_config: LLMConfig


RESPONSE_TYPE = TypeVar("RESPONSE_TYPE")


class ClientResponse(TypedDict, Generic[RESPONSE_TYPE]):
    response: Optional[RESPONSE_TYPE]
    error: Optional[Exception]


TokenScore = Dict[str, float]


class TextCompletionResponse(TypedDict):
    answer: str
    token_scores: Optional[List[TokenScore]]


# class TextCompletionWithLogitsResponse(TextCompletionResponse):
#     token_scores: List[TokenScore]


class ContextLengthExceededError(Exception):
    def __init__(self, message: str, extra_characters: Optional[int] = None):
        super().__init__(message)
        self.extra_characters = extra_characters


class TextCompletionClientBaseConfig(TypedDict):
    model_name: str


class OpenAiClientConfig(TextCompletionClientBaseConfig):
    openai_api_key: str
    openai_org: str
    openai_api_type: Optional[str]
    openai_api_base: Optional[str]
    openai_api_version: Optional[str]
    openai_temperature: float


class TextCompletionClientConfig(OpenAiClientConfig):
    ...


class TextCompletionClient(ABC):
    def __init__(self, **config: Unpack[TextCompletionClientConfig]):
        raise NotImplementedError

    @abstractmethod
    async def complete(
        self,
        text_completion_requests: List[TextCompletionRequest],
    ) -> List[ClientResponse[TextCompletionResponse]]:
        raise NotImplementedError


# class TextCompletionWithLogitsClient(TextCompletionClient):
#     @abstractmethod
#     async def complete(
#         self,
#         text_completion_requests: List[TextCompletionRequest],
#     ) -> List[ClientResponse[TextCompletionWithLogitsResponse]]:
#         raise NotImplementedError