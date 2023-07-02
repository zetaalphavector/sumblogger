from abc import ABC, abstractmethod

from src.types.text_completion import TextCompletionUsecaseConfig


class TextCompletionUsecaseConfigRepository(ABC):
    @abstractmethod
    async def get_by(self, usecase: str, variant: str) -> TextCompletionUsecaseConfig:
        raise NotImplementedError
