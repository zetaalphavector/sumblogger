from abc import ABC, abstractmethod
from typing import List, TypedDict

import httpx
import torch
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class TextModelInferenceResponse(TypedDict):
    text: str


class TextModelInferenceClient(ABC):
    @abstractmethod
    async def infer(self, inputs: List[str]) -> List[TextModelInferenceResponse]:
        raise NotImplementedError


class HuggingFaceSeq2SeqLMApiClient(TextModelInferenceClient):
    __BATCH_SIZE = 2
    __CLIENT_BATCH_SIZE = 50

    def __init__(
        self,
        model_base_url: str,
        model_api_key: str,
        batch_size: int = __BATCH_SIZE,
    ):
        self.__api_url = f"{model_base_url}/generate"
        self.__auth_headers = {"api_key": model_api_key}
        self.__batch_size = batch_size

    async def infer(
        self,
        inputs: List[str],
        **infer_params,
    ) -> List[TextModelInferenceResponse]:
        batches = [
            inputs[i : i + self.__CLIENT_BATCH_SIZE]
            for i in range(0, len(inputs), self.__CLIENT_BATCH_SIZE)
        ]
        outputs = []
        for batch in batches:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    self.__api_url,
                    json={
                        "inputs": batch,
                        "batch_size": self.__batch_size,
                        "model_params": {**infer_params},
                    },
                    headers=self.__auth_headers,
                    timeout=12000,
                )
                r.raise_for_status()
                response = r.json()

                outputs.extend(response["outputs"])

        return [TextModelInferenceResponse(text=output) for output in outputs]


class HuggingFaceSeq2SeqLMLocalClient(TextModelInferenceClient):
    def __init__(self, model_name):
        self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.__model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(
            self.__device
        )

    async def infer(
        self, inputs: List[str], **infer_params
    ) -> List[TextModelInferenceResponse]:
        batch_size = 32
        batches = [
            inputs[i : i + batch_size] for i in range(0, len(inputs), batch_size)
        ]
        outputs = []

        for batch in tqdm(batches):
            batch_input_ids = self.__tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
            ).input_ids.to(self.__device)

            batch_outputs = self.__model.generate(batch_input_ids, **infer_params)
            batch_outputs = self.__tokenizer.batch_decode(
                batch_outputs, skip_special_tokens=True
            )
            outputs.extend(batch_outputs)

        return [TextModelInferenceResponse(text=output) for output in outputs]
