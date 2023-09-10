from typing import List, Optional

from src.services.text_completion.client import ClientResponse, TextCompletionResponse
from src.services.text_completion.service_factory import TextCompletionServiceFactory
from src.services.text_completion.service_template import TextCompletionServiceTemplate
from src.types.text_completion import PromptParams


class BlogSurroundings(PromptParams):
    title: str
    intro: str
    conclusion: str


@TextCompletionServiceFactory.register("blog_surroundings")
class BlogSurroundingsService(TextCompletionServiceTemplate):
    def service_response_from(
        self,
        text_completion_response: ClientResponse[TextCompletionResponse],
        params: PromptParams,
        output_params: List[str],
    ) -> Optional[BlogSurroundings]:

        if text_completion_response.response is None:
            return None
        else:
            response = text_completion_response.response["answer"]
            return BlogSurroundings(
                title=self.__title_from(response),
                intro=self.__intro_from(response),
                conclusion=self.__conclusion_from(response),
            )

    def __title_from(self, response: str) -> str:
        if "A. Title: " in response:
            return response.split("A. Title: ")[1].split("B. Introduction:")[0]
        else:
            return response.split("A.")[1].split("B.")[0]

    def __intro_from(self, response: str) -> str:
        if "B. Introduction:" in response:
            return response.split("B. Introduction:")[1].split("C. Conclusion:")[0]
        else:
            return response.split("B.")[1].split("C.")[0]

    def __conclusion_from(self, response: str) -> str:
        if "C. Conclusion:" in response:
            return response.split("C. Conclusion:")[1]
        else:
            return response.split("C.")[1]
