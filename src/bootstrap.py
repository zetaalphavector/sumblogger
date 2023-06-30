from zav.message_bus import Bootstrap
from zav.message_bus.bootstrap import BootstrapDependency

from src.adapters.text_completion_repo.file_repo import (
    FileTextCompletionUsecaseConfigRepository,
)
from src.handlers import CommandHandlerRegistry, EventHandlerRegistry

text_completion_usecase_config_repo = FileTextCompletionUsecaseConfigRepository(
    config_dir="src/services/text_completion/configuration"
)

bootstrap_deps = [
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
