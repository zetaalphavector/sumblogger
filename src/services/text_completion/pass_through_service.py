from typing import List, Optional, cast

from src.services.text_completion.client import ClientResponse, TextCompletionResponse
from src.services.text_completion.service_factory import TextCompletionServiceFactory
from src.services.text_completion.service_template import TextCompletionServiceTemplate
from src.services.text_completion.types import PromptParams


@TextCompletionServiceFactory.register("pass_through")
class PassThroughTextCompletionService(TextCompletionServiceTemplate):
    def service_response_from(
        self,
        text_completion_response: ClientResponse[TextCompletionResponse],
        params: PromptParams,
        output_params: List[str],
    ) -> Optional[PromptParams]:

        if text_completion_response["response"] is None:
            return None
        else:
            return cast(
                PromptParams,
                {
                    **params,
                    output_params[0]: text_completion_response["response"]["answer"],
                },
            )

    def postprocess(
        self,
        service_responses: List[PromptParams],
        params_list: List[PromptParams],
        output_params: List[str],
    ) -> List[PromptParams]:
        return service_responses
