from typing import List, Union

import numpy as np
from evaluate import load

from tools.experimentation.metrics.calculator import SummarizationMetricCalculator


class BertScoreMetricCalculator(SummarizationMetricCalculator):
    def __init__(self) -> None:
        self.__bertscore = load("bertscore")

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

        score = self.__bertscore.compute(
            predictions=output_summaries,
            references=targets,
            lang="en-sci",
        )
        if score is None:
            raise ValueError("BertScore is None")

        return np.mean(score["f1"])
