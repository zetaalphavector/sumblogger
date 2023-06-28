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


def expected_two_batch_summaries_output(number_of_docs):
    return [
        {
            "output_params_list": [
                {
                    "document": document_for(i),
                    "first_batch_summary": summary_for(i),
                }
                for i in range(number_of_docs)
            ]
        },
        {
            "output_params_list": [
                {
                    "document": document_for(i),
                    "second_batch_summary": summary_for(i),
                }
                for i in range(number_of_docs)
            ]
        },
    ]


def expected_flattened_two_batch_summaries_output(number_of_docs):
    return [
        {
            "output_params_list": [
                {
                    "document": 2 * [document_for(i)],
                    "first_batch_summary": [summary_for(i)],
                    "second_batch_summary": [summary_for(i)],
                }
                for i in range(number_of_docs)
            ]
        }
    ]


def expected_two_step_summary_output(number_of_docs):
    return [
        {
            "input_document": document_for(i),
            "summary_of_summary": f"This is the summary of the summary {i}",
            "summary": summary_for(i),
        }
        for i in range(number_of_docs)
    ]


def two_step_single_doc_summary_chain(number_of_docs):
    return [
        {
            **summary_request_for(number_of_docs, should_flatten=False),
            "params_mapping": {
                "document": "input_document",
                "summary": "document",
            },
        },
        {
            "usecase": "single_doc_summary",
            "variant": "scitldr_vanilla",
            "prompt_params_list": [],
            "params_mapping": {
                "summary": "summary_of_summary",
                "document": "summary",
            },
            "should_flatten": False,
        },
    ]


def two_step_multi_doc_summary_chain(number_of_docs):
    return [
        {
            **summary_request_for(number_of_docs, should_flatten=True),
            "params_mapping": {
                "document": "input_documents",
                "summary": "ref_documents",
            },
        },
        {
            "usecase": "multi_doc_summary",
            "variant": "multi_xscience_two_step",
            "prompt_params_list": [
                {
                    "main_document": "This is the main document",
                    "number_of_words": 100,
                    "ref_document_ids": [str(i) for i in range(number_of_docs)],
                }
            ],
            "params_mapping": {
                "summary": "multi_doc_summary",
            },
        },
    ]


def expected_two_step_multi_doc_summary_output(number_of_docs):
    return [
        {
            "input_documents": [document_for(id) for id in range(number_of_docs)],
            "ref_documents": [summary_for(i) for i in range(number_of_docs)],
            "main_document": "This is the main document",
            "number_of_words": 100,
            "ref_document_ids": [str(i) for i in range(number_of_docs)],
            "multi_doc_summary": "This is the multi-doc summary",
        }
    ]


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
        single_doc_summary_client_mock = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.return_value = (
            single_doc_summary_client_mock
        )
        single_doc_summary_client_mock.complete.side_effect = lambda _: [
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

        single_doc_summary_client_mock.complete.asssert_has_calls(
            [
                mock.call(text_completion_request_for(document_for(index)))
                for index in range(number_of_docs)
            ],
        )

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_chain_two_text_completion_requests_in_a_map_reduce_fashion(
        self,
        text_completion_client_factory_mock,
        test_client,
        base_path,
        text_completion_client_mock,
    ):
        number_of_docs = 2
        payload = {
            "chain_usecase_forms": two_step_multi_doc_summary_chain(number_of_docs)
        }

        single_doc_summary_client_mock = text_completion_client_mock.create()
        multi_doc_summary_client_mock = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            single_doc_summary_client_mock,
            multi_doc_summary_client_mock,
        ]
        single_doc_summary_client_mock.complete.side_effect = lambda _: [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        multi_doc_summary_client_mock.complete.side_effect = lambda _: [
            text_completion_response_from("This is the multi-doc summary")
        ]

        resp = await test_client.post(
            f"{base_path}/text_completion/chain",
            data=json.dumps(payload),
        )

        assert resp.status_code == 200
        json_resp = resp.json()

        assert json_resp[
            "output_params_list"
        ] == expected_two_step_multi_doc_summary_output(number_of_docs)

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_chain_two_text_completion_requests(
        self,
        text_completion_client_factory_mock,
        test_client,
        base_path,
        text_completion_client_mock,
    ):
        number_of_docs = 2
        payload = {
            "chain_usecase_forms": two_step_single_doc_summary_chain(number_of_docs)
        }

        single_doc_summary_client_mock_1 = text_completion_client_mock.create()
        single_doc_summary_client_mock_2 = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_2,
        ]
        single_doc_summary_client_mock_1.complete.side_effect = lambda _: [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        single_doc_summary_client_mock_2.complete.side_effect = lambda _: [
            text_completion_response_from(f"This is the summary of the summary {index}")
            for index in range(number_of_docs)
        ]

        resp = await test_client.post(
            f"{base_path}/text_completion/chain",
            data=json.dumps(payload),
        )

        assert resp.status_code == 200
        json_resp = resp.json()

        assert json_resp["output_params_list"] == expected_two_step_summary_output(
            number_of_docs
        )

    @mark.parametrize(
        ("number_of_docs", "should_flatten", "expected_output"),
        [
            (2, False, expected_two_batch_summaries_output(2)),
            (2, True, expected_flattened_two_batch_summaries_output(2)),
        ],
    )
    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_execute_text_completion_requests_in_parallel(
        self,
        text_completion_client_factory_mock,
        number_of_docs,
        should_flatten,
        expected_output,
        test_client,
        base_path,
        text_completion_client_mock,
    ):
        number_of_docs = 2
        payload = {
            "parallel_usecase_forms": [
                {
                    **summary_request_for(number_of_docs, should_flatten=False),
                    "params_mapping": {
                        "summary": "first_batch_summary",
                    },
                },
                {
                    **summary_request_for(number_of_docs, should_flatten=False),
                    "params_mapping": {
                        "summary": "second_batch_summary",
                    },
                },
            ],
            "should_flatten": should_flatten,
        }

        single_doc_summary_client_mock_1 = text_completion_client_mock.create()
        single_doc_summary_client_mock_2 = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_2,
        ]
        single_doc_summary_client_mock_1.complete.side_effect = lambda _: [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        single_doc_summary_client_mock_2.complete.side_effect = lambda _: [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]

        resp = await test_client.post(
            f"{base_path}/text_completion/parallel",
            data=json.dumps(payload),
        )
        print(f"resp: {resp.json()}")
        assert resp.status_code == 200
        json_resp = resp.json()

        assert json_resp["usecase_items"] == expected_output

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_execute_two_chains_in_parallel(
        self,
        text_completion_client_factory_mock,
        test_client,
        base_path,
        text_completion_client_mock,
    ):
        number_of_docs = 2
        payload = {
            "parallel_usecase_forms": [
                {
                    "chain_usecase_forms": two_step_single_doc_summary_chain(
                        number_of_docs
                    )
                },
                {
                    "chain_usecase_forms": two_step_single_doc_summary_chain(
                        number_of_docs
                    )
                },
            ],
            "should_flatten": False,
        }

        single_doc_summary_client_mock_1 = text_completion_client_mock.create()
        single_doc_summary_client_mock_2 = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_2,
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_2,
        ]
        single_doc_summary_client_mock_1.complete.side_effect = lambda _: [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        single_doc_summary_client_mock_2.complete.side_effect = lambda _: [
            text_completion_response_from(f"This is the summary of the summary {index}")
            for index in range(number_of_docs)
        ]

        resp = await test_client.post(
            f"{base_path}/text_completion/parallel",
            data=json.dumps(payload),
        )

        assert resp.status_code == 200
        json_resp = resp.json()

        assert json_resp["usecase_items"] == [
            {"output_params_list": expected_two_step_summary_output(number_of_docs)},
            {"output_params_list": expected_two_step_summary_output(number_of_docs)},
        ]
