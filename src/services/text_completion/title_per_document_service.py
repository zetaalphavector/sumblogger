from typing import List, Optional, cast

from src.services.text_completion.client import ClientResponse, TextCompletionResponse
from src.services.text_completion.service_factory import TextCompletionServiceFactory
from src.services.text_completion.service_template import TextCompletionServiceTemplate
from src.services.text_completion.types import PromptParams


@TextCompletionServiceFactory.register("title_per_document")
class TitlePerDocumentService(TextCompletionServiceTemplate):
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
                    output_params[0]: self.__titles_from(
                        text_completion_response["response"]["answer"],
                        params,
                    ),
                },
            )

    def __titles_from(self, answer: str, params: PromptParams) -> List[str]:
        titles = []
        for index, _ in enumerate(params["documents"]):
            title = answer.split(f"{index+1}.")[1].split("\n")[0].strip()
            titles.append(title)
        return titles
