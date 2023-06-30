import re
from typing import List, cast

from src.services.text_completion.client import (
    ClientResponse,
    TextCompletionClient,
    TextCompletionRequest,
    TextCompletionResponse,
)
from src.services.text_completion.config_parser import TextCompletionConfigParser
from src.services.text_completion.pass_through_service import (
    PassThroughTextCompletionService,
)
from src.services.text_completion.service_factory import TextCompletionServiceFactory
from src.services.text_completion.types import (
    ChatMessage,
    ChatMessageSender,
    PromptParams,
)


@TextCompletionServiceFactory.register("refined_multi_doc_summary")
class RefinedMultiDocSummaryCompletionService(PassThroughTextCompletionService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__quality_check_to_fun = {
            "no_citations": self.__no_citations,
            "too_long": self.__is_too_long,
            "too_many_sentences": self.__too_many_sentences,
        }
        self.__quality_check_to_refinement_message_template = {
            "no_citations": "Not all documents are cited in the summary. You should cite them all, while keeping the length of the summary at {{ number_of_words }} words.",  # noqa: E501
            "too_long": "Shorten the summary to fit in around {{ number_of_words }} words, while keeping it informative and fluent. Also, do not forget to include citations to all documents.",  # noqa: E501
            "too_many_sentences": "Merge together some sentences in order to make the summary more fluent, while keeping the length around {{ number_of_words }} words.",  # noqa: E501
        }

    async def postprocess_one(
        self,
        service_response: PromptParams,
        client_response: ClientResponse[TextCompletionResponse],
        client_request: TextCompletionRequest,
        client: TextCompletionClient,
        output_params: List[str],
    ) -> PromptParams:

        if client_response.response is None:
            raise Exception(f"Text Completion Error: {client_response.error}")

        target_number_of_words = service_response["number_of_words"]
        retries_left = service_response["retries"]

        while retries_left > 0:
            retries_left -= 1
            summary = service_response["summary"]
            for check_type, check_fn in self.__quality_check_to_fun.items():
                if check_fn(summary, target_number_of_words):
                    msg = self.__create_refinement_message(service_response, check_type)
                    updated_client_request = self.__enhance_bot_conversation(
                        summary, msg, client_request
                    )
                    client_response = await client.complete(updated_client_request)
                    if client_response.response is None:
                        raise Exception(
                            f"Text Completion Error: {client_response.error}"
                        )
                    service_response["summary"] = client_response.response["answer"]
                    break

        return service_response

    def __create_refinement_message(self, service_response, check_type) -> str:
        msg_template = self.__quality_check_to_refinement_message_template[check_type]

        refinement_message = TextCompletionConfigParser.parse_template(
            msg_template,
            cast(
                PromptParams, {"number_of_words": service_response["number_of_words"]}
            ),
        )
        if refinement_message is None:
            raise Exception(f"Unknown refinement message type: {check_type}")

        return refinement_message

    def __enhance_bot_conversation(
        self,
        summary: str,
        refinement_message: str,
        client_request: TextCompletionRequest,
    ) -> TextCompletionRequest:
        chat_messages = [
            ChatMessage(
                sender=ChatMessageSender.BOT,
                content=summary,
            ),
            ChatMessage(
                sender=ChatMessageSender.USER,
                content=refinement_message,
            ),
        ]

        client_request = client_request.copy()
        if client_request["llm_config"].text_completion_config.bot_conversation is None:
            raise Exception("Bot conversation is not defined")
        client_request[
            "llm_config"
        ].text_completion_config.bot_conversation.messages.extend(chat_messages)
        return client_request

    def __is_too_long(self, summary: str, word_limit: int) -> bool:
        return len(summary.split()) > 1.4 * word_limit

        raise NotImplementedError

    def __number_of_citations(self, text: str) -> int:
        return len(re.findall(r"\[d\d+\]", text)) + len(
            re.findall(r"\[d\d+(,\s*d\d+)+\]", text)
        )

    def __no_citations(self, summary: str, docs_size: int) -> bool:
        return self.__number_of_citations(summary) < 0.8 * docs_size

    def __too_many_sentences(self, summary: str) -> bool:
        citations = self.__number_of_citations(summary)
        return len(re.findall(r"\.\s", summary)) > 0.9 * citations
