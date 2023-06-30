from typing import List, Optional, cast

from typing_extensions import TypedDict

from src.services.text_completion.client import (
    ClientResponse,
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
from src.services.text_completion.types import (
    LLMConfig,
    PromptParams,
    TextCompletionConfig,
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

    def __parse_config(
        self, text_completion_config: TextCompletionConfig, params: PromptParams
    ) -> TextCompletionConfig:
        return TextCompletionConfigParser.parse(
            text_completion_config,
            params,
        )

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

    def text_completion_configs_from(
        self, config_template: TextCompletionConfig, params_list: List[PromptParams]
    ) -> List[TextCompletionConfig]:
        return [self.__parse_config(config_template, params) for params in params_list]

    def text_completion_requests_from(
        self, llm_config_template: LLMConfig, params_list: List[PromptParams]
    ) -> List[TextCompletionRequest]:
        text_completion_configs = TextCompletionConfigParser.parse_many(
            llm_config_template.text_completion_config, params_list
        )
        llm_config_merged = LLMConfig.parse_obj(
            {
                **llm_config_template.dict(exclude={"text_completion_config"}),
                "text_completion_config": text_completion_configs[0],
            }
        )

        return [TextCompletionRequest(llm_config=llm_config_merged)]

    def service_response_from(
        self,
        text_completion_response: ClientResponse[TextCompletionResponse],
        params: PromptParams,
        output_params: List[str],
    ) -> Optional[PromptParams]:
        raise NotImplementedError

    def service_responses_from(
        self,
        text_completion_responses: List[ClientResponse[TextCompletionResponse]],
        params_list: List[PromptParams],
        output_params: List[str],
    ) -> Optional[List[PromptParams]]:
        responses = []
        for client_response, params in zip(text_completion_responses, params_list):
            if client_response["response"] is None:
                return None

            responses.append(
                self.service_response_from(client_response, params, output_params)
            )
        return responses

    def postprocess(
        self,
        service_responses: List[PromptParams],
        params_list: List[PromptParams],
        output_params: List[str],
    ) -> List[PromptParams]:
        raise NotImplementedError

    async def execute(
        self, request: TextCompletionServiceRequest
    ) -> Optional[List[PromptParams]]:
        for param in request["usecase_config"].usecase_params:
            for params in request["params_list"]:
                if param not in params:
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
            text_completion_requests = self.text_completion_requests_from(
                llm_config, request["params_list"]
            )
            client = self.text_completion_client_from(llm_identifier)
            text_completion_responses = await client.complete(text_completion_requests)
            service_responses = self.service_responses_from(
                text_completion_responses,
                request["params_list"],
                request["usecase_config"].output_params,
            )
            if service_responses is None:
                return None

            service_responses = self.postprocess(
                service_responses,
                request["params_list"],
                request["usecase_config"].output_params,
            )

            if request["should_flatten"]:
                flattened = {}
                for response in service_responses:
                    for key, value in response.items():
                        if key not in flattened:
                            flattened[key] = []
                        flattened[key].append(value)
                return [cast(PromptParams, flattened)]
            else:
                return service_responses

        except Exception as e:
            raise e
