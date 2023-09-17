from unittest.mock import AsyncMock

import pytest

from src.adapters.text_completion_repo.file_repo import (
    FileTextCompletionUsecaseConfigRepository,
)
from src.services.text_completion.client import TextCompletionClient
from src.services.text_completion.client_factory import TextCompletionClientFactory


@pytest.fixture(scope="session")
def mock_text_completion_usecase_config_repo():
    test_config_dir = "tests/resources/text_completion_usecase_configs"
    return FileTextCompletionUsecaseConfigRepository(config_dir=test_config_dir)


@pytest.fixture()
def text_completion_client_mock():
    class CreateClientMockWrapper:
        def create(self):
            return AsyncMock(TextCompletionClient)

    return CreateClientMockWrapper()


@pytest.fixture
def text_completion_client_factory_mock(mocker):
    return mocker.Mock(spec=TextCompletionClientFactory)
