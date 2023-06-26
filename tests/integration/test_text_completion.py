import json
from unittest.mock import patch

from src.services.text_completion.client import (
    ClientResponse,
    TextCompletionRequest,
    TextCompletionResponse,
)
from src.services.text_completion.types import (
    BotConversation,
    ChatMessage,
    ChatMessageSender,
    LLMConfig,
    TextCompletionConfig,
)

from ..conftest import text_completion_client_factory_mock


class TestTextCompletionUsecase:
    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    async def test_should_use_the_prompt_configured_by_the_usecase(
        self,
        text_completion_client_factory_mock,
        test_client,
        base_path,
        text_completion_client_mock,
    ):
        input_doc = "This is a document"
        expected_output = "This is the summary"

        text_completion_client_factory_mock.create.return_value = (
            text_completion_client_mock
        )
        text_completion_client_mock.complete.side_effect = lambda _: [
            ClientResponse(
                response=TextCompletionResponse(
                    answer="This is the summary", token_scores=None
                ),
                error=None,
            )
        ]

        payload = {
            "usecase": "single_doc_summary",
            "variant": "scitldr_vanilla",
            "prompt_params": {
                "document": input_doc,
            },
        }

        resp = await test_client.post(
            f"{base_path}/text_completion/pass_through",
            data=json.dumps(payload),
        )

        assert resp.status_code == 200
        json_resp = resp.json()

        assert json_resp["response"] == expected_output

        text_completion_client_mock.complete.assert_called_once_with(
            [
                TextCompletionRequest(
                    llm_config=LLMConfig(
                        call_params={
                            "temperature": 0.0,
                            "max_tokens": 100,
                        },
                        text_completion_config=TextCompletionConfig(
                            prompt_template=None,
                            bot_conversation=BotConversation(
                                bot_setup_description=None,
                                messages=[
                                    ChatMessage(
                                        sender=ChatMessageSender.USER,
                                        content=f"{input_doc}\nSummarize the above article in 1 sentence.",  # noqa: E501
                                    )
                                ],
                            ),
                        ),
                    )
                )
            ]
        )
