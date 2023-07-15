from typing import List, Optional, cast

import backoff
from typing_extensions import TypedDict

from src.services.text_completion.client import (
    ClientResponse,
    RateLimitExceededError,
    ServiceUnavailableError,
    TextCompletionClient,
    TextCompletionClientConfig,
    TextCompletionRequest,
    TextCompletionResponse,
)
from src.services.text_completion.client_factory import (
    TextCompletionClientFactory,
    TextCompletionModelType,
    TextCompletionProviderName,
)
from src.services.text_completion.config_parser import TextCompletionConfigParser
from src.services.text_completion.service_factory import TextCompletionService
from src.types.text_completion import (
    LLMConfig,
    PromptParams,
    TextCompletionServiceRequest,
)


class TextModelParams(TypedDict):
    model_type: TextCompletionModelType
    provider_name: TextCompletionProviderName
    model_name: str


class TextCompletionServiceTemplate(TextCompletionService):
    def __init__(
        self,
        text_completion_client_config: TextCompletionClientConfig,
    ):
        self.__text_completion_client_config = text_completion_client_config

    def service_response_from(
        self,
        text_completion_response: ClientResponse[TextCompletionResponse],
        params: PromptParams,
        output_params: List[str],
    ) -> Optional[PromptParams]:
        raise NotImplementedError

    async def execute(
        self, request: TextCompletionServiceRequest
    ) -> Optional[PromptParams]:
        for param in request["usecase_config"].usecase_params:
            if param not in request["params"]:
                raise Exception(
                    f"Param {param} not given for usecase {request['usecase_config'].usecase}"  # noqa: E501
                )

        llms = iter(request["usecase_config"].llm_identifier_2_config.items())
        llm_identifier, llm_config = next(llms)
        if llm_identifier is None or llm_config is None:
            raise Exception(
                f"No LLM given for usecase {request['usecase_config'].usecase}"
            )

        try:
            client = self.text_completion_client_from(llm_identifier)
            service_response = await self.execute_one(
                request["params"],
                llm_config,
                request["usecase_config"].output_params,
                client,
            )

            if service_response is None:
                return None

            return service_response

        except Exception as e:
            raise e

    @backoff.on_exception(
        backoff.expo,
        (RateLimitExceededError, ServiceUnavailableError),
        max_time=300,
    )
    async def execute_one(
        self,
        params: PromptParams,
        llm_config_template: LLMConfig,
        output_params: List[str],
        client: TextCompletionClient,
    ) -> Optional[PromptParams]:
        client_request = self.text_completion_request_from(llm_config_template, params)
        client_response = await client.complete(client_request)
        service_response = self.service_response_from(
            client_response,
            params,
            output_params,
        )
        if service_response is None:
            raise Exception("TextCompletionService response is None")

        service_response = await self.postprocess_one(
            service_response,
            params,
            client_response,
            client_request,
            client,
            output_params,
        )

        return service_response

    async def postprocess_one(
        self,
        service_response: PromptParams,
        params: PromptParams,
        client_response: ClientResponse[TextCompletionResponse],
        client_request: TextCompletionRequest,
        client: TextCompletionClient,
        output_params: List[str],
    ) -> PromptParams:
        return service_response

    def __model_params_from(self, model_identifier: str) -> TextModelParams:
        model_type, provider_name, model_name = model_identifier.split(":")
        return TextModelParams(
            model_type=TextCompletionModelType(model_type),
            provider_name=TextCompletionProviderName(provider_name),
            model_name=model_name,
        )

    def text_completion_client_from(
        self, model_identifier: str
    ) -> TextCompletionClient:
        model_params = self.__model_params_from(model_identifier)
        return TextCompletionClientFactory.create(
            provider_name=model_params["provider_name"],
            model_type=model_params["model_type"],
            config=cast(
                TextCompletionClientConfig,
                {
                    **self.__text_completion_client_config,
                    "model_name": model_params["model_name"],
                },
            ),
        )

    def text_completion_request_from(
        self, llm_config_template: LLMConfig, params: PromptParams
    ) -> TextCompletionRequest:
        text_completion_config = TextCompletionConfigParser.parse(
            llm_config_template.text_completion_config, params
        )
        llm_config_merged = LLMConfig.parse_obj(
            {
                **llm_config_template.dict(exclude={"text_completion_config"}),
                "text_completion_config": text_completion_config,
            }
        )

        return TextCompletionRequest(llm_config=llm_config_merged)
