from typing import Dict, List

from src.adapters.zav_search_client import Client
from src.adapters.zav_search_client.api.documents import document_search
from src.adapters.zav_search_client.models.document_search_document_types_item import (
    DocumentSearchDocumentTypesItem,
)
from src.adapters.zav_search_client.models.document_search_retrieval_method import (
    DocumentSearchRetrievalMethod,
)
from src.adapters.zav_search_client.models.document_search_retrieval_unit import (
    DocumentSearchRetrievalUnit,
)
from src.adapters.zav_search_client.models.document_search_sort import (
    DocumentSearchSort,
)
from src.adapters.zav_search_client.models.document_search_sort_order_item import (
    DocumentSearchSortOrderItem,
)
from src.adapters.zav_search_client.models.search_engine_string import (
    SearchEngineString,
)
from src.adapters.zav_search_client.types import UNSET
from src.services.retrieval.client import SearchApiClient


class ZavSearchClient(SearchApiClient):
    def __init__(self, base_url: str):
        self.client = Client(
            base_url=base_url,
            timeout=10,
            raise_on_unexpected_status=True,
            verify_ssl=False,
        )

    async def get_by_ids(self, ids: List[str]) -> Dict:
        search_response = await document_search.asyncio(
            client=self.client,
            search_engine=SearchEngineString.ZETA_ALPHA,
            tenant="zetaalpha",
            retrieval_unit=DocumentSearchRetrievalUnit.DOCUMENT,
            query_string="",
            retrieval_method=DocumentSearchRetrievalMethod.KEYWORD,
            sources=[],
            doc_ids=ids,
            document_types=[DocumentSearchDocumentTypesItem.DOCUMENT],
            sort_order=[DocumentSearchSortOrderItem.DATE],
            sort=DocumentSearchSort(date=UNSET),
            page_size=len(ids),
        )
        if search_response is None:
            return {}

        return search_response.to_dict()

    async def get(self, query_text) -> Dict:
        raise NotImplementedError
