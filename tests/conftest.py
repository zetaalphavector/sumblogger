from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
from zav.message_bus import Bootstrap
from zav.message_bus.bootstrap import BootstrapDependency

from src.adapters.text_completion_client.factory import TextCompletionClientFactory
from src.adapters.text_completion_repo.file_repo import (
    FileTextCompletionUsecaseConfigRepository,
)
from src.app import app, routers, setup_api
from src.bootstrap import CommandHandlerRegistry, EventHandlerRegistry
from src.services.text_completion.client import TextCompletionClient


@pytest.fixture(scope="session")
def mock_text_completion_usecase_config_repo():
    test_config_dir = "tests/resources/text_completion_usecase_configs"
    return FileTextCompletionUsecaseConfigRepository(config_dir=test_config_dir)


@pytest.fixture(scope="session")
def mock_bootstrap(mock_text_completion_usecase_config_repo):
    return Bootstrap(
        dependencies=[
            BootstrapDependency(
                name="text_completion_usecase_config_repo",
                value=mock_text_completion_usecase_config_repo,
            ),
        ],
        command_handler_registry=CommandHandlerRegistry,
        event_handler_registry=EventHandlerRegistry,
    )


@pytest.fixture()
def base_path():
    return "/v1"


@pytest.fixture(scope="session")
def test_client(mock_bootstrap):
    setup_api(app=app, bootstrap=mock_bootstrap, routers=routers)
    client = AsyncClient(app=app, base_url="http://test")
    yield client


@pytest.fixture()
def text_completion_client_mock():
    class CreateClientMockWrapper:
        def create(self):
            return AsyncMock(TextCompletionClient)

    return CreateClientMockWrapper()


@pytest.fixture
def text_completion_client_factory_mock(mocker):
    return mocker.Mock(spec=TextCompletionClientFactory)
