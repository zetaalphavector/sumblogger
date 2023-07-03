from typing import Dict, List, Optional

from src.services.retrieval.client import SearchApiClient
from src.types.documents import Document


class RetrieveDocumentsService:
    def __init__(self, search_client: SearchApiClient):
        self.search_client = search_client

    async def get_by_ids(self, ids: List[str]) -> Optional[List[Document]]:
        documents = []
        batches = [ids[i : i + 10] for i in range(0, len(ids), 10)]
        for batch_ids in batches:
            search_response = await self.search_client.get_by_ids(batch_ids)
            if search_response is None or "hits" not in search_response:
                return None

            batch_docs = [self.__document_from(hit) for hit in search_response["hits"]]
            documents.extend(batch_docs)

        return documents

    def __document_from(self, hit: Dict) -> Document:
        return Document(
            id=hit["guid"],
            title=hit["metadata"]["title"],
            abstract=hit["metadata"]["abstract"],
            content=hit["metadata"]["abstract"],
            url=hit["uri"],
            authors=[creator["full_name"] for creator in hit["metadata"]["creator"]],
            year=hit["metadata"]["date"],
            created_at=hit["metadata"]["created"],
        )

    async def get(self, query_text) -> Dict:
        raise NotImplementedError
