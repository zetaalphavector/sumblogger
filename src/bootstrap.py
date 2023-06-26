from zav.message_bus import Bootstrap
from zav.message_bus.bootstrap import BootstrapDependency

from src.adapters.text_completion_client.factory import TextCompletionClientConfig
from src.adapters.text_completion_repo.file_repo import (
    FileTextCompletionUsecaseConfigRepository,
)
from src.handlers import CommandHandlerRegistry, EventHandlerRegistry
from src.services.text_completion.pass_through_service import (
    PassThroughTextCompletionService,
)
from src.settings import (
    OPENAI_API_BASE,
    OPENAI_API_KEY,
    OPENAI_API_TYPE,
    OPENAI_API_VERSION,
    OPENAI_DEFAULT_MODEL,
    OPENAI_DEFAULT_TEMPERATURE,
    OPENAI_ORG,
)

text_completion_client_config = TextCompletionClientConfig(
    openai_api_key=OPENAI_API_KEY,
    openai_org=OPENAI_ORG,
    openai_api_base=OPENAI_API_BASE,
    openai_api_type=OPENAI_API_TYPE,
    openai_api_version=OPENAI_API_VERSION,
    model_name=OPENAI_DEFAULT_MODEL,
    openai_temperature=OPENAI_DEFAULT_TEMPERATURE,
)
pass_through_text_completion_service = PassThroughTextCompletionService(
    text_completion_client_config=text_completion_client_config
)

text_completion_usecase_config_repo = FileTextCompletionUsecaseConfigRepository(
    config_dir="src/services/text_completion/configuration"
)

bootstrap_deps = [
    BootstrapDependency(
        name="pass_through_text_completion_service",
        value=pass_through_text_completion_service,
    ),
    BootstrapDependency(
        name="text_completion_usecase_config_repo",
        value=text_completion_usecase_config_repo,
    ),
]

bootstrap = Bootstrap(
    dependencies=bootstrap_deps,
    command_handler_registry=CommandHandlerRegistry,
    event_handler_registry=EventHandlerRegistry,
)
