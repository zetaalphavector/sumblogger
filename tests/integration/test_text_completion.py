import json
from unittest import mock
from unittest.mock import patch

from pytest import mark

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


def document_for(doc_id: int):
    return f"This is document {doc_id}"


def summary_for(doc_id: int):
    return f"This is the summary for document {doc_id}"


def summary_request_for(number_of_docs: int, should_flatten: bool = False):
    return {
        "usecase": "single_doc_summary",
        "variant": "scitldr_vanilla",
        "prompt_params_list": [
            {
                "document": document_for(doc_id),
            }
            for doc_id in range(number_of_docs)
        ],
        "params_mapping": {
            "summary": "single_doc_summary",
        },
        "should_flatten": should_flatten,
    }


def expected_output_for(number_of_docs: int):
    return [
        {
            "document": document_for(doc_id),
            "single_doc_summary": summary_for(doc_id),
        }
        for doc_id in range(number_of_docs)
    ]


def expected_flattened_output_for(number_of_docs: int):
    return [
        {
            "document": [document_for(doc_id) for doc_id in range(number_of_docs)],
            "single_doc_summary": [
                summary_for(doc_id) for doc_id in range(number_of_docs)
            ],
        }
    ]


def text_completion_response_from(answer):
    return ClientResponse(
        response=TextCompletionResponse(answer=answer, token_scores=None), error=None
    )


def text_completion_request_for(document):
    return TextCompletionRequest(
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
                            content=f"{document}\nSummarize the above article in 1 sentence.",  # noqa: E501
                        )
                    ],
                ),
            ),
        )
    )


class TestTextCompletionUsecase:
    @mark.parametrize(
        "number_of_docs, should_flatten, expected_output",
        [
            (
                2,
                True,
                expected_flattened_output_for(number_of_docs=2),
            ),
            (
                2,
                False,
                expected_output_for(number_of_docs=2),
            ),
        ],
    )
    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_use_the_prompt_configured_by_the_usecase(
        self,
        text_completion_client_factory_mock,
        number_of_docs,
        should_flatten,
        expected_output,
        test_client,
        base_path,
        text_completion_client_mock,
    ):

        payload = summary_request_for(
            number_of_docs=number_of_docs,
            should_flatten=should_flatten,
        )

        text_completion_client_factory_mock.create.return_value = (
            text_completion_client_mock
        )
        text_completion_client_mock.complete.side_effect = lambda _: [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]

        resp = await test_client.post(
            f"{base_path}/text_completion/pass_through",
            data=json.dumps(payload),
        )

        assert resp.status_code == 200
        json_resp = resp.json()

        assert json_resp["output_params_list"] == expected_output

        text_completion_client_mock.complete.asssert_has_calls(
            [
                mock.call(text_completion_request_for(document_for(index)))
                for index in range(number_of_docs)
            ],
        )
