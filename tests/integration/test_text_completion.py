from typing import List, Union
from unittest import mock
from unittest.mock import patch

from pytest import mark

from src.handlers import text_completion
from src.handlers.commands import (
    ExecuteTextCompletionSingleUsecase,
    ExecuteTextCompletionUsecases,
    UsecaseCommandsExecutionType,
)
from src.services.text_completion.client import (
    ClientResponse,
    TextCompletionRequest,
    TextCompletionResponse,
)
from src.types.text_completion import (
    BotConversation,
    ChatMessage,
    ChatMessageSender,
    LLMConfig,
    TextCompletionConfig,
)

from ..conftest import text_completion_client_factory_mock

NUMBER_OF_SUMMARY_WORDS = 300


def document_for(doc_id: int):
    return f"This is document {doc_id}"


def summary_for(doc_id: int):
    return f"This is the summary for document {doc_id}"


def summary_usecase_for(
    number_of_docs: int,
    params_mapping: dict = {
        "summary": "single_doc_summary",
    },
) -> ExecuteTextCompletionUsecases:
    usecase_commands: List[
        Union[ExecuteTextCompletionSingleUsecase, ExecuteTextCompletionUsecases]
    ] = [
        ExecuteTextCompletionSingleUsecase(
            usecase="single_doc_summary",
            variant="scitldr_vanilla",
            prompt_params={
                "document": document_for(doc_id),
            },
            params_mapping=params_mapping,
        )
        for doc_id in range(number_of_docs)
    ]
    return ExecuteTextCompletionUsecases(
        execution_type=UsecaseCommandsExecutionType.PARALLEL,
        prompt_params={},
        usecase_commands=usecase_commands,
        params_mapping=params_mapping,
    )


def second_step_multidoc_summary_request_for(
    variant: str,
    output_var_name: str,
) -> ExecuteTextCompletionSingleUsecase:
    return ExecuteTextCompletionSingleUsecase(
        usecase="multi_doc_summary",
        variant=variant,
        prompt_params={
            "number_of_words": NUMBER_OF_SUMMARY_WORDS,
        },
        params_mapping={
            "summary": output_var_name,
            "documents": "single_doc_summaries",
        },
    )


def expected_output_for(number_of_docs: int):
    return {
        "document": [document_for(doc_id) for doc_id in range(number_of_docs)],
        "single_doc_summary": [summary_for(doc_id) for doc_id in range(number_of_docs)],
    }


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


def expected_two_step_summary_output(number_of_docs):
    return {
        "document": [summary_for(i) for i in range(number_of_docs)],
        "input_document": [document_for(i) for i in range(number_of_docs)],
        "summary_of_summary": [
            f"This is the summary of the summary {i}" for i in range(number_of_docs)
        ],
        "summary": [summary_for(i) for i in range(number_of_docs)],
    }


def two_step_single_doc_summary_chain(
    number_of_docs,
) -> List[Union[ExecuteTextCompletionUsecases, ExecuteTextCompletionSingleUsecase]]:
    usecase_commands = [
        ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.PARALLEL,
            prompt_params={},
            usecase_commands=[
                ExecuteTextCompletionUsecases(
                    execution_type=UsecaseCommandsExecutionType.CHAIN,
                    prompt_params={},
                    usecase_commands=[
                        ExecuteTextCompletionSingleUsecase(
                            usecase="single_doc_summary",
                            variant="scitldr_vanilla",
                            prompt_params={
                                "document": document_for(doc_id),
                            },
                            params_mapping={
                                "summary": "document",
                                "document": "input_document",
                            },
                        ),
                        ExecuteTextCompletionSingleUsecase(
                            usecase="single_doc_summary",
                            variant="scitldr_vanilla",
                            prompt_params={},
                            params_mapping={
                                "summary": "summary_of_summary",
                                "document": "summary",
                            },
                        ),
                    ],
                )
                for doc_id in range(number_of_docs)
            ],
        )
    ]
    return usecase_commands


def two_step_multi_doc_summary_chain(number_of_docs):
    return [
        summary_usecase_for(
            number_of_docs,
            {"document": "input_documents", "summary": "ref_documents"},
        ),
        ExecuteTextCompletionSingleUsecase(
            usecase="multi_doc_summary",
            variant="multi_xscience_two_step",
            prompt_params={
                "main_document": "This is the main document",
                "number_of_words": NUMBER_OF_SUMMARY_WORDS,
                "ref_document_ids": [str(i) for i in range(number_of_docs)],
            },
            params_mapping={
                "summary": "multi_doc_summary",
            },
        ),
    ]


def expected_two_step_multi_doc_summary_output(number_of_docs):
    return {
        "input_documents": [document_for(id) for id in range(number_of_docs)],
        "ref_documents": [summary_for(i) for i in range(number_of_docs)],
        "main_document": "This is the main document",
        "number_of_words": NUMBER_OF_SUMMARY_WORDS,
        "ref_document_ids": [str(i) for i in range(number_of_docs)],
        "multi_doc_summary": "This is the multi-doc summary",
    }


class TestTextCompletionUsecase:
    @mark.parametrize(
        "number_of_docs, expected_output",
        [
            (
                2,
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
        expected_output,
        mock_text_completion_usecase_config_repo,
        text_completion_client_mock,
    ):

        payload = ExecuteTextCompletionUsecases(
            prompt_params={},
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            usecase_commands=[summary_usecase_for(number_of_docs)],
        )
        single_doc_summary_client_mock = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.return_value = (
            single_doc_summary_client_mock
        )
        single_doc_summary_client_mock.complete.side_effect = [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]

        response = await text_completion.execute(
            payload, mock_text_completion_usecase_config_repo
        )

        assert response["output_params"] == expected_output

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
        mock_text_completion_usecase_config_repo,
        text_completion_client_mock,
    ):
        number_of_docs = 2
        payload = ExecuteTextCompletionUsecases(
            prompt_params={},
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            usecase_commands=two_step_multi_doc_summary_chain(number_of_docs),
        )

        single_doc_summary_client_mock = text_completion_client_mock.create()
        multi_doc_summary_client_mock = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = number_of_docs * [
            single_doc_summary_client_mock
        ] + [multi_doc_summary_client_mock]
        single_doc_summary_client_mock.complete.side_effect = [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        multi_doc_summary_client_mock.complete.side_effect = [
            text_completion_response_from("This is the multi-doc summary")
        ]

        response = await text_completion.execute(
            payload, mock_text_completion_usecase_config_repo
        )

        assert response["output_params"] == expected_two_step_multi_doc_summary_output(
            number_of_docs
        )

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_chain_two_text_completion_requests(
        self,
        text_completion_client_factory_mock,
        mock_text_completion_usecase_config_repo,
        text_completion_client_mock,
    ):
        number_of_docs = 2
        payload = ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            prompt_params={},
            usecase_commands=two_step_single_doc_summary_chain(number_of_docs),
        )

        single_doc_summary_client_mock_1 = text_completion_client_mock.create()
        single_doc_summary_client_mock_2 = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_2,
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_2,
        ]

        single_doc_summary_client_mock_1.complete.side_effect = [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        single_doc_summary_client_mock_2.complete.side_effect = [
            text_completion_response_from(f"This is the summary of the summary {index}")
            for index in range(number_of_docs)
        ]

        response = await text_completion.execute(
            payload, mock_text_completion_usecase_config_repo
        )

        assert response["output_params"] == expected_two_step_summary_output(
            number_of_docs
        )

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_execute_text_completion_requests_in_parallel(
        self,
        text_completion_client_factory_mock,
        mock_text_completion_usecase_config_repo,
        text_completion_client_mock,
    ):
        number_of_docs = 2
        payload = ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.PARALLEL,
            prompt_params={},
            usecase_commands=[
                summary_usecase_for(number_of_docs, {"summary": "first_batch_summary"}),
                summary_usecase_for(
                    number_of_docs, {"summary": "second_batch_summary"}
                ),
            ],
        )

        single_doc_summary_client_mock_1 = text_completion_client_mock.create()
        single_doc_summary_client_mock_2 = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_1,
            single_doc_summary_client_mock_2,
            single_doc_summary_client_mock_2,
        ]
        single_doc_summary_client_mock_1.complete.side_effect = [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        single_doc_summary_client_mock_2.complete.side_effect = [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]

        response = await text_completion.execute(
            payload, mock_text_completion_usecase_config_repo
        )

        assert response["output_params"] == {
            "document": [
                [document_for(i) for i in range(number_of_docs)],
                [document_for(i) for i in range(number_of_docs)],
            ],
            "first_batch_summary": [summary_for(i) for i in range(number_of_docs)],
            "second_batch_summary": [summary_for(i) for i in range(number_of_docs)],
        }

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_split_a_chain_in_two_parallel_usecases(
        self,
        text_completion_client_factory_mock,
        mock_text_completion_usecase_config_repo,
        text_completion_client_mock,
    ):
        number_of_docs = 3
        payload = ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            prompt_params={},
            usecase_commands=[
                summary_usecase_for(
                    number_of_docs,
                    {"summary": "documents", "document": "input_documents"},
                ),
                ExecuteTextCompletionUsecases(
                    execution_type=UsecaseCommandsExecutionType.PARALLEL,
                    prompt_params={},
                    usecase_commands=[
                        second_step_multidoc_summary_request_for(
                            "intro_paragraph", "intro_summary"
                        ),
                        second_step_multidoc_summary_request_for(
                            "detailed_paragraph", "detailed_summary"
                        ),
                    ],
                ),
            ],
        )
        single_doc_summary_client_mock = text_completion_client_mock.create()
        multi_doc_summary_client_mock_1 = text_completion_client_mock.create()
        multi_doc_summary_client_mock_2 = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = number_of_docs * [
            single_doc_summary_client_mock
        ] + [multi_doc_summary_client_mock_1, multi_doc_summary_client_mock_2]

        single_doc_summary_client_mock.complete.side_effect = [
            text_completion_response_from(summary_for(index))
            for index in range(number_of_docs)
        ]
        multi_doc_summary_client_mock_1.complete.side_effect = [
            text_completion_response_from("This is the intro summary")
        ]
        multi_doc_summary_client_mock_2.complete.side_effect = [
            text_completion_response_from("This is the detailed summary")
        ]

        response = await text_completion.execute(
            payload, mock_text_completion_usecase_config_repo
        )

        assert response["output_params"] == {
            "documents": [summary_for(i) for i in range(number_of_docs)],
            "input_documents": [document_for(i) for i in range(number_of_docs)],
            "single_doc_summaries": [
                [summary_for(i) for i in range(number_of_docs)],
                [summary_for(i) for i in range(number_of_docs)],
            ],
            "intro_summary": "This is the intro summary",
            "detailed_summary": "This is the detailed summary",
            "number_of_words": [NUMBER_OF_SUMMARY_WORDS, NUMBER_OF_SUMMARY_WORDS],
        }

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_execute_a_custom_usecase(
        self,
        text_completion_client_factory_mock,
        mock_text_completion_usecase_config_repo,
        text_completion_client_mock,
    ):
        number_of_docs = 3
        payload = ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            prompt_params={},
            usecase_commands=[
                ExecuteTextCompletionSingleUsecase(
                    usecase="title_generation",
                    variant="title_per_intro_summary",
                    prompt_params={
                        "documents": [
                            document_for(doc_id) for doc_id in range(number_of_docs)
                        ],
                    },
                )
            ],
        )
        text_comletion_client_mock = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            text_comletion_client_mock,
        ]

        text_comletion_client_mock.complete.side_effect = [
            text_completion_response_from("1. Title A\n2. Title B\n3. Title C")
        ]

        response = await text_completion.execute(
            payload, mock_text_completion_usecase_config_repo
        )

        assert response["output_params"] == {
            "documents": [document_for(i) for i in range(number_of_docs)],
            "titles": ["Title A", "Title B", "Title C"],
        }

    @patch(
        "src.services.text_completion.service_template.TextCompletionClientFactory",
        return_value=text_completion_client_factory_mock,
    )
    @mark.asyncio
    async def test_should_execute_a_custom_usecase_that_refines_the_output(
        self,
        text_completion_client_factory_mock,
        mock_text_completion_usecase_config_repo,
        text_completion_client_mock,
    ):
        number_of_docs = 3
        payload = ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            prompt_params={},
            usecase_commands=[
                ExecuteTextCompletionSingleUsecase(
                    usecase="multi_doc_summary",
                    variant="refine_summary",
                    prompt_params={
                        "documents": [
                            document_for(doc_id) for doc_id in range(number_of_docs)
                        ],
                        "number_of_words": NUMBER_OF_SUMMARY_WORDS,
                        "retries": 1,
                    },
                )
            ],
        )
        text_comletion_client_mock = text_completion_client_mock.create()
        text_completion_client_factory_mock.create.side_effect = [
            text_comletion_client_mock,
        ]

        text_comletion_client_mock.complete.side_effect = [
            text_completion_response_from("This summary has no citations."),
            text_completion_response_from(
                "The refined summary has all the needed citations [0], [1], [2]"
            ),
        ]

        response = await text_completion.execute(
            payload, mock_text_completion_usecase_config_repo
        )

        assert response["output_params"] == {
            "documents": [document_for(i) for i in range(number_of_docs)],
            "summary": "The refined summary has all the needed citations [0], [1], [2]",  # noqa
            "number_of_words": NUMBER_OF_SUMMARY_WORDS,
            "retries": 1,
        }
