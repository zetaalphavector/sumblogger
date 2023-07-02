from typing import List, Union

import numpy as np
from evaluate import load

from tools.experimentation.metrics.calculator import SummarizationMetricCalculator


class BleurtMetricCalculator(SummarizationMetricCalculator):
    def __init__(self) -> None:
        self.__bleurt = load("bleurt", module_type="metric")

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

        bleurt_output = self.__bleurt.compute(
            predictions=output_summaries,
            references=targets,
        )
        if bleurt_output is None:
            raise ValueError("BLEURT is None")

        return np.mean(bleurt_output["scores"])
