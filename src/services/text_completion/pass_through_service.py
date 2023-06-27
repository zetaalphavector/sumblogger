from typing import Any, Dict, List, Optional

from src.services.text_completion.client import ClientResponse, TextCompletionResponse
from src.services.text_completion.service_template import TextCompletionServiceTemplate
from src.services.text_completion.types import TextCompletionServiceResponse


class PassThroughTextCompletionServiceResponse(TextCompletionServiceResponse):
    answers: List[str]


class PassThroughTextCompletionService(
    TextCompletionServiceTemplate[PassThroughTextCompletionServiceResponse]
):
    def service_responses_from(
        self,
        text_completion_responses: List[ClientResponse[TextCompletionResponse]],
        output_params: List[str],
    ) -> Optional[List[Dict[str, Any]]]:
        answers = []
        for client_response in text_completion_responses:
            if client_response["response"] is None:
                return None
            else:
                answers.append(
                    {output_params[0]: client_response["response"]["answer"]}
                )

        return answers

    def postprocess(
        self,
        service_responses: Optional[List[Dict[str, Any]]],
        output_params: List[str],
    ) -> Optional[List[Dict[str, Any]]]:
        return service_responses
