from abc import ABC, abstractmethod
from typing import Dict, List


class SearchApiClient(ABC):
    @abstractmethod
    async def get_by_ids(self, ids: List[str]) -> Dict:
        raise NotImplementedError

    @abstractmethod
    async def get(self, query_text) -> Dict:
        raise NotImplementedError
