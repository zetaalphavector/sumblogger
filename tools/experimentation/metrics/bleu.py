from typing import List, Union

import numpy as np
from evaluate import load

from tools.experimentation.metrics.calculator import SummarizationMetricCalculator


class BleuMetricCalculator(SummarizationMetricCalculator):
    def __init__(self) -> None:
        self.__bleu = load("bleu")

    def execute(
        self,
        documents: List[str],
        gold_summaries: Union[List[str], List[List[str]]],
        output_summaries: List[str],
    ) -> float:
        # if isinstance(gold_summaries[0], list):
        #     targets = gold_summaries[0]
        # else:
        targets = gold_summaries

        score = self.__bleu.compute(
            predictions=output_summaries,
            references=targets,
        )
        if score is None:
            raise ValueError("BLEU is None")

        return np.mean(score["bleu"])
