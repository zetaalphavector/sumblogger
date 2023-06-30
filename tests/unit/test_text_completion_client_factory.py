from pytest import mark

from src.adapters.text_completion_client.factory import (
    TextCompletionClientFactory,
    TextCompletionModelType,
    TextCompletionProviderName,
)
from src.adapters.text_completion_client.openai_clients import (
    OpenAiChatClient,
    OpenAiPromptClient,
    OpenAiPromptWithLogitsClient,
)
from src.settings import DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG


class TestTextCompletionClientFactory:
    @mark.parametrize(
        "provider_name, model_type, expected_instance_type",
        [
            (
                TextCompletionProviderName.OPENAI,
                TextCompletionModelType.PROMPT,
                OpenAiPromptClient,
            ),
            (
                TextCompletionProviderName.OPENAI,
                TextCompletionModelType.CHAT,
                OpenAiChatClient,
            ),
            (
                TextCompletionProviderName.OPENAI,
                TextCompletionModelType.PROMPT_WITH_LOGITS,
                OpenAiPromptWithLogitsClient,
            ),
        ],
    )
    def test_should_return_the_same_requested_client_for_the_same_config(
        self,
        provider_name,
        model_type,
        expected_instance_type,
    ):
        client = TextCompletionClientFactory.create(
            provider_name=provider_name,
            model_type=model_type,
            config=DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG,
        )

        assert isinstance(client, expected_instance_type)

        client_2 = TextCompletionClientFactory.create(
            provider_name=provider_name,
            model_type=model_type,
            config=DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG,
        )
        assert client == client_2
