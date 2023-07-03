from zav.message_bus import Bootstrap
from zav.message_bus.bootstrap import BootstrapDependency

from src.adapters.text_completion_repo.file_repo import (
    FileTextCompletionUsecaseConfigRepository,
)
from src.adapters.zav_search_client.zav_search_client import ZavSearchClient
from src.handlers import CommandHandlerRegistry, EventHandlerRegistry
from src.services.retrieval.retrieve_documents import RetrieveDocumentsService
from src.settings import ZAV_SEARCH_API_BASE_URL

text_completion_usecase_config_repo = FileTextCompletionUsecaseConfigRepository(
    config_dir="src/services/text_completion/configuration"
)
retrieve_docs_service = RetrieveDocumentsService(
    ZavSearchClient(ZAV_SEARCH_API_BASE_URL)
)

bootstrap_deps = [
    BootstrapDependency(
        name="text_completion_usecase_config_repo",
        value=text_completion_usecase_config_repo,
    ),
    BootstrapDependency(
        name="retrieve_docs_service",
        value=retrieve_docs_service,
    ),
]

bootstrap = Bootstrap(
    dependencies=bootstrap_deps,
    command_handler_registry=CommandHandlerRegistry,
    event_handler_registry=EventHandlerRegistry,
)
