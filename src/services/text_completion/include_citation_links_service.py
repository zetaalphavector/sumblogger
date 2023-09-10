import re
from typing import List

from src.services.text_completion.client import (
    ClientResponse,
    TextCompletionClient,
    TextCompletionRequest,
    TextCompletionResponse,
)
from src.services.text_completion.pass_through_service import (
    PassThroughTextCompletionService,
)
from src.services.text_completion.service_factory import TextCompletionServiceFactory
from src.types.text_completion import PromptParams


@TextCompletionServiceFactory.register("include_citation_links")
class RefinedMultiDocSummaryCompletionService(PassThroughTextCompletionService):
    async def postprocess_one(
        self,
        service_response: PromptParams,
        params: PromptParams,
        client_response: ClientResponse[TextCompletionResponse],
        client_request: TextCompletionRequest,
        client: TextCompletionClient,
        output_params: List[str],
    ) -> PromptParams:

        if client_response.response is None:
            raise Exception(f"Text Completion Error: {client_response.error}")

        summary = service_response["summary"]
        sentences = summary.split(". ")
        if self.__number_of_citations(sentences[0]) == 0:
            summary = ". ".join(sentences[1:])
        available_index = 1
        for index, doc_url in enumerate(params["document_urls"]):
            possible_citations = [
                f"[d{index}]",
                f"[d{index},",
                f", d{index}]",
                f", d{index} ,",
            ]
            citation = None
            for c in possible_citations:
                if c in summary:
                    citation = c
                    break
            if doc_url is None:
                raise Exception(f"No URL found for: {input}")

            if citation is not None:
                # remove "d" from citation wherever it appears
                citation_without_d = citation.replace(f"d{index}", str(available_index))
                available_index += 1
                summary = summary.replace(
                    citation,
                    self.__link_and_hover_text(
                        citation_without_d,
                        f"[{params['document_titles'][index]}]: {params['documents'][index]}",  # noqa: E501
                        doc_url,
                    ),
                )
        service_response["summary"] = summary
        return service_response

    def __number_of_citations(self, text: str) -> int:
        return len(re.findall(r"\[d\d+\]", text)) + len(
            re.findall(r"\[d\d+(,\s*d\d+)+\]", text)
        )

    def __link_and_hover_text(self, text: str, hover_text: str, link: str):
        hover_text = hover_text.replace('"', "")
        return f'[{text}]({link} "{hover_text}")'
