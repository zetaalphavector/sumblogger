import enum
from typing import List, Union


class SummarizationMetric(enum.Enum):
    ROUGE_1 = "rouge1"
    ROUGE_2 = "rouge2"
    ROUGE_L = "rougeL"
    ROUGE_1_STOPWORDS = "rouge1_stopwords"
    ROUGE_2_STOPWORDS = "rouge2_stopwords"
    ROUGE_L_STOPWORDS = "rougeL_stopwords"
    BLEU = "bleu"
    BLEURT = "bleurt"
    METEOR = "meteor"
    BERT_SCORE = "bert_score"


class SummarizationMetricCalculator:
    def execute(
        self,
        documents: List[str],
        gold_summaries: Union[List[str], List[List[str]]],
        output_summaries: List[str],
    ) -> float:
        raise NotImplementedError
