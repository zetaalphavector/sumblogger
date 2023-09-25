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

        filtered_summaries = []
        for summary in output_summaries:
            word_tokens = word_tokenize(summary)
            filtered_words = [
                word for word in word_tokens if word.lower() not in self.__stop_words
            ]
            filtered_text = " ".join(filtered_words)
            filtered_summaries.append(filtered_text)

        filtered_gold_summaries = []
        for summary in gold_summaries:
            filtered_summary = []
            for sentence in summary:
                word_tokens = word_tokenize(sentence)
                filtered_words = [
                    word
                    for word in word_tokens
                    if word.lower() not in self.__stop_words
                ]
                filtered_text = " ".join(filtered_words)
                filtered_summary.append(filtered_text)
            filtered_gold_summaries.append(filtered_summary)

        # output_summaries = filtered_summaries

        scores = rouge_score(
            filtered_summaries,
            filtered_gold_summaries,
            rouge_keys=self.__rouge_key,
            accumulate="best",
            use_stemmer=True,
        )

        return scores[f"{self.__rouge_key}_fmeasure"].item()
