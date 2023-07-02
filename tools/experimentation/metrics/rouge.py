from typing import List, Union

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from torchmetrics.functional.text.rouge import rouge_score

from tools.experimentation.metrics.calculator import SummarizationMetricCalculator


class RougeMetricCalculator(SummarizationMetricCalculator):
    def __init__(self, rouge_key: str) -> None:
        self.__rouge_key = rouge_key
        nltk.download("stopwords")
        self.__stop_words = set(stopwords.words("english"))

    def execute(
        self,
        documents: List[str],
        gold_summaries: Union[List[str], List[List[str]]],
        output_summaries: List[str],
    ) -> float:

        scores = rouge_score(
            output_summaries,
            gold_summaries,
            rouge_keys=self.__rouge_key,
            accumulate="best",
            use_stemmer=True,
        )

        return scores[f"{self.__rouge_key}_fmeasure"].item()
