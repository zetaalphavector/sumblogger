from src.adapters.text_completion_repo.file_repo import (
    FileTextCompletionUsecaseConfigRepository,
)
from src.adapters.zav_search_client.zav_search_client import ZavSearchClient
from src.services.retrieval.retrieve_documents import RetrieveDocumentsService
from src.settings import ZAV_SEARCH_API_BASE_URL

TEXT_COMPLETION_USECASE_CONFIG_REPO = FileTextCompletionUsecaseConfigRepository(
    config_dir="src/services/text_completion/configuration"
)
RETRIEVE_DOCS_SERVICE = RetrieveDocumentsService(
    ZavSearchClient(ZAV_SEARCH_API_BASE_URL)
)
