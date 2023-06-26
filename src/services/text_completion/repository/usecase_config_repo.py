from abc import ABC, abstractmethod

from src.services.text_completion.types import TextCompletionUsecaseConfig


class TextCompletionUsecaseConfigRepository(ABC):
    @abstractmethod
    async def get_by(self, usecase: str, variant: str) -> TextCompletionUsecaseConfig:
        raise NotImplementedError
