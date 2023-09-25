from typing import List

from src.settings import HF_MODEL_API_KEY, HF_MODEL_API_URL
from tools.experimentation.finetuned_models.hf_client import (
    HuggingFaceSeq2SeqLMApiClient,
    HuggingFaceSeq2SeqLMLocalClient,
    TextModelInferenceClient,
)


class HFFineTunedSummarizationModel:
    def __init__(self, client: TextModelInferenceClient, **infer_params):
        self.__client = client
        self.__infer_params = infer_params

    async def execute(self, requests: List[str]) -> List[str]:
        responses = await self.__client.infer(
            [f"{self.input_prefix()}{request}" for request in requests],
            **self.__infer_params,
        )

        return [response["text"] for response in responses]

    def input_prefix(self) -> str:
        return ""


class CattsScitldrFineTunedSummarizationModel(HFFineTunedSummarizationModel):
    def __init__(self):
        super().__init__(
            HuggingFaceSeq2SeqLMLocalClient(
                model_name="lrakotoson/scitldr-catts-xsum-ao"
            ),
            num_beams=4,
            length_penalty=0.2,
        )


class PegasusFineTunedSummarizationModel(HFFineTunedSummarizationModel):
    def __init__(self):
        super().__init__(
            HuggingFaceSeq2SeqLMApiClient(
                model_base_url=HF_MODEL_API_URL,
                model_api_key=HF_MODEL_API_KEY,
            ),
            num_beams=8,
            length_penalty=0.8,
            max_length=256,
        )


class T5FineTunedSummarizationModel(HFFineTunedSummarizationModel):
    def __init__(self):
        super().__init__(
            HuggingFaceSeq2SeqLMLocalClient(
                model_name="HenryHXR/t5-base-finetuned-scitldr-only-abstract"
            ),
            length_penalty=2.0,
            max_length=200,
            min_length=30,
            no_repeat_ngram_size=3,
            num_beams=4,
        )

    def input_prefix(self) -> str:
        return "summarize: "
