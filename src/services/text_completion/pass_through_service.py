from typing import List, Optional

from src.services.text_completion.client import ClientResponse, TextCompletionResponse
from src.services.text_completion.service_template import TextCompletionServiceTemplate
from src.services.text_completion.types import TextCompletionServiceResponse


class PassThroughTextCompletionServiceResponse(TextCompletionServiceResponse):
    answers: List[str]


class PassThroughTextCompletionService(
    TextCompletionServiceTemplate[PassThroughTextCompletionServiceResponse]
):
    def service_response_from(
        self, text_completion_responses: List[ClientResponse[TextCompletionResponse]]
    ) -> Optional[PassThroughTextCompletionServiceResponse]:
        answers = []
        for client_response in text_completion_responses:
            if client_response["response"] is None:
                return None
            else:
                answers.append(client_response["response"]["answer"])

        return PassThroughTextCompletionServiceResponse(answers=answers)

    def postprocess(
        self, service_response: PassThroughTextCompletionServiceResponse
    ) -> PassThroughTextCompletionServiceResponse:
        return service_response
