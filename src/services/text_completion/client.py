from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, List, Optional, TypeVar

from typing_extensions import TypedDict, Unpack

from src.types.text_completion import LLMConfig


class TextCompletionRequest(TypedDict):
    llm_config: LLMConfig


TokenScore = Dict[str, float]

RESPONSE_TYPE = TypeVar("RESPONSE_TYPE")


@dataclass
class ClientResponse(Generic[RESPONSE_TYPE]):
    response: Optional[RESPONSE_TYPE]
    error: Optional[Exception]


class TextCompletionResponse(TypedDict):
    answer: str
    token_scores: Optional[List[TokenScore]]


# class ClientResponse(TypedDict):
#     response: Optional[TextCompletionResponse]
#     error: Optional[Exception]


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
        text_completion_request: TextCompletionRequest,
    ) -> ClientResponse[TextCompletionResponse]:
        raise NotImplementedError


# class TextCompletionWithLogitsClient(TextCompletionClient):
#     @abstractmethod
#     async def complete(
#         self,
#         text_completion_requests: List[TextCompletionRequest],
#     ) -> List[ClientResponse[TextCompletionWithLogitsResponse]]:
#         raise NotImplementedError
