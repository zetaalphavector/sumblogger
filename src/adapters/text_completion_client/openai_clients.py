import re
from datetime import datetime
from typing import Optional

import openai
from typing_extensions import Unpack

from src.services.text_completion.client import (
    ClientResponse,
    ContextLengthExceededError,
    OpenAiClientConfig,
    RateLimitExceededError,
    ServiceUnavailableError,
    TextCompletionClient,
    TextCompletionRequest,
    TextCompletionResponse,
)
from src.services.text_completion.client_factory import (
    TextCompletionClientFactory,
    TextCompletionModelType,
    TextCompletionProviderName,
)
from src.types.text_completion import BotConversation, ChatMessageSender

CHARACTERS_PER_TOKEN = 4


def __extract_int_from_text(pattern: str, text: str) -> Optional[int]:
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return None


def __context_length_exception_from(error_message: str) -> ContextLengthExceededError:
    max_tokens_limit = __extract_int_from_text(
        r"maximum context length is (\d+) tokens", error_message
    )
    requested_tokens = __extract_int_from_text(r"requested (\d+) tokens", error_message)
    extra_characters = (
        (requested_tokens - max_tokens_limit) * CHARACTERS_PER_TOKEN
        if max_tokens_limit and requested_tokens
        else None
    )
    return ContextLengthExceededError(
        message=error_message,
        extra_characters=extra_characters,
    )


@TextCompletionClientFactory.register(
    provider_name=TextCompletionProviderName.OPENAI,
    model_type=TextCompletionModelType.PROMPT,
)
class OpenAiPromptClient(TextCompletionClient):
    def __init__(self, **config: Unpack[OpenAiClientConfig]):
        self.__organization = config["openai_org"]
        self.__api_key = config["openai_api_key"]
        self.__api_version = config["openai_api_version"] or openai.api_version
        self.__api_base = config["openai_api_base"] or openai.api_base
        self.__api_type = config["openai_api_type"] or openai.api_type
        self.__model_name = config["model_name"]
        self.__model_temperature = config["openai_temperature"]

    async def complete(
        self, request: TextCompletionRequest
    ) -> ClientResponse[TextCompletionResponse]:
        return await self.__complete_single_request(request)

    async def __complete_single_request(
        self, request: TextCompletionRequest
    ) -> ClientResponse[TextCompletionResponse]:
        prompt_template = request["llm_config"].text_completion_config.prompt_template

        if prompt_template is None:
            raise ValueError("Prompt template is required")

        try:
            response = await openai.Completion.acreate(
                **{
                    "model": self.__model_name,
                    "prompt": prompt_template,
                    "temperature": self.__model_temperature,
                    "organization": self.__organization,
                    "api_key": self.__api_key,
                    "api_version": self.__api_version,
                    "api_base": self.__api_base,
                    "api_type": self.__api_type,
                    **request["llm_config"].call_params,
                }
            )
            return ClientResponse(
                response=TextCompletionResponse(
                    answer=response.choices[0].text.strip(),
                    token_scores=None,
                ),
                error=None,
            )
        except openai.InvalidRequestError as e:
            if e.code == "context_length_exceeded":
                return ClientResponse(
                    response=None,
                    error=__context_length_exception_from(str(e.user_message)),
                )
            else:
                raise e
        except openai.error.RateLimitError as e:  # type: ignore
            raise RateLimitExceededError(e)
        except openai.error.ServiceUnavailableError as e:  # type: ignore
            raise ServiceUnavailableError(e)
        except Exception as e:
            return ClientResponse(response=None, error=e)


@TextCompletionClientFactory.register(
    provider_name=TextCompletionProviderName.OPENAI,
    model_type=TextCompletionModelType.PROMPT_WITH_LOGITS,
)
class OpenAiPromptWithLogitsClient(TextCompletionClient):
    __INCLUDE_LOGPROBS_FOR_MOST_LIKELY_TOKEN = 0

    def __init__(self, **config: Unpack[OpenAiClientConfig]):
        self.__organization = config["openai_org"]
        self.__api_key = config["openai_api_key"]
        self.__api_version = config["openai_api_version"] or openai.api_version
        self.__api_base = config["openai_api_base"] or openai.api_base
        self.__api_type = config["openai_api_type"] or openai.api_type
        self.__model_name = config["model_name"]
        self.__model_temperature = config["openai_temperature"]

    async def complete(
        self, request: TextCompletionRequest
    ) -> ClientResponse[TextCompletionResponse]:
        return await self.__complete_single_request(request)

    async def __complete_single_request(
        self, request: TextCompletionRequest
    ) -> ClientResponse[TextCompletionResponse]:
        prompt_template = request["llm_config"].text_completion_config.prompt_template

        if prompt_template is None:
            raise ValueError("Prompt template is required")

        try:
            response = await openai.Completion.acreate(
                **{
                    "model": self.__model_name,
                    "prompt": prompt_template,
                    "logprobs": self.__INCLUDE_LOGPROBS_FOR_MOST_LIKELY_TOKEN,
                    "temperature": self.__model_temperature,
                    "organization": self.__organization,
                    "api_key": self.__api_key,
                    "api_version": self.__api_version,
                    "api_base": self.__api_base,
                    "api_type": self.__api_type,
                    **request["llm_config"].call_params,
                }
            )
            return self.__text_completion_response_from(response)

        except openai.InvalidRequestError as e:
            if e.code == "context_length_exceeded":
                return ClientResponse(
                    response=None,
                    error=__context_length_exception_from(str(e.user_message)),
                )
            else:
                raise e

        except openai.error.RateLimitError as e:  # type: ignore
            raise RateLimitExceededError(e)
        except openai.error.ServiceUnavailableError as e:  # type: ignore
            raise ServiceUnavailableError(e)
        except Exception as e:
            return ClientResponse(response=None, error=e)

    def __text_completion_response_from(
        self, openai_response
    ) -> ClientResponse[TextCompletionResponse]:
        answer_choice = openai_response.answer.choices[0]
        return ClientResponse(
            response=TextCompletionResponse(
                answer=answer_choice.text.strip(),
                token_scores=[
                    {token: token_logprob}
                    for token, token_logprob in zip(
                        answer_choice.logprobs.tokens,
                        answer_choice.logprobs.token_logprobs,
                    )
                ],
            ),
            error=None,
        )


@TextCompletionClientFactory.register(
    provider_name=TextCompletionProviderName.OPENAI,
    model_type=TextCompletionModelType.CHAT,
)
class OpenAiChatClient(TextCompletionClient):
    TOKENS_PER_CHARACTER = 4
    __SENDER_TO_ROLE = {
        ChatMessageSender.BOT: "assistant",
        ChatMessageSender.USER: "user",
    }

    def __init__(self, **config: Unpack[OpenAiClientConfig]):
        self.__organization = config["openai_org"]
        self.__api_key = config["openai_api_key"]
        self.__api_version = config["openai_api_version"] or openai.api_version
        self.__api_base = config["openai_api_base"] or openai.api_base
        self.__api_type = config["openai_api_type"] or openai.api_type
        self.__model_name = config["model_name"]
        self.__model_temperature = config["openai_temperature"]

    async def complete(
        self, request: TextCompletionRequest
    ) -> ClientResponse[TextCompletionResponse]:
        return await self.__complete_single_request(request)

    async def __complete_single_request(
        self, request: TextCompletionRequest
    ) -> ClientResponse[TextCompletionResponse]:
        bot_conversation = request["llm_config"].text_completion_config.bot_conversation
        if bot_conversation is None:
            raise ValueError("Bot conversation is required")

        messages = self.__messages_from(bot_conversation)
        # with open(f"chat_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", "w") as f:
        #     f.write("\n".join([m["content"] for m in messages]))

        try:
            response = await openai.ChatCompletion.acreate(
                **{
                    "model": self.__model_name,
                    "messages": messages,
                    "temperature": self.__model_temperature,
                    "organization": self.__organization,
                    "api_key": self.__api_key,
                    "api_version": self.__api_version,
                    "api_base": self.__api_base,
                    "api_type": self.__api_type,
                    **request["llm_config"].call_params,
                }
            )
            return ClientResponse(
                response=TextCompletionResponse(
                    answer=response.choices[0]["message"]["content"],
                    token_scores=None,
                ),
                error=None,
            )
        except openai.InvalidRequestError as e:
            if e.code == "context_length_exceeded":
                raise __context_length_exception_from(str(e.user_message))
            else:
                raise e
        except openai.error.RateLimitError as e:  # type: ignore
            raise RateLimitExceededError(e)
        except openai.error.ServiceUnavailableError as e:  # type: ignore
            raise ServiceUnavailableError(e)

        except Exception as e:
            raise e

    def __messages_from(self, conversation: BotConversation):
        messages = [
            {
                "role": self.__SENDER_TO_ROLE[message.sender],
                "content": message.content,
            }
            for message in conversation.messages
        ]

        if conversation.bot_setup_description is not None:
            system_setup_message = {
                "role": "system",
                "content": conversation.bot_setup_description,
            }

            messages = [system_setup_message] + messages

        return messages
