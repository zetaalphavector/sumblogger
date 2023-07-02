import asyncio
import os
import time
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict

import pandas as pd
from tqdm import tqdm

from tools.experimentation.metrics.bert_score import BertScoreMetricCalculator
from tools.experimentation.metrics.bleu import BleuMetricCalculator
from tools.experimentation.metrics.calculator import (
    SummarizationMetric,
    SummarizationMetricCalculator,
)
from tools.experimentation.metrics.rouge import RougeMetricCalculator
from tools.experimentation.run import summaries_csv_filename_from

METRIC_2_CALCULATOR: Dict[SummarizationMetric, SummarizationMetricCalculator] = {
    SummarizationMetric.ROUGE_1: RougeMetricCalculator(rouge_key="rouge1"),
    SummarizationMetric.ROUGE_2: RougeMetricCalculator(rouge_key="rouge2"),
    SummarizationMetric.ROUGE_L: RougeMetricCalculator(rouge_key="rougeL"),
    SummarizationMetric.BLEU: BleuMetricCalculator(),
    SummarizationMetric.BERT_SCORE: BertScoreMetricCalculator(),
}


current_dir = os.path.dirname(os.path.realpath(__file__))
RESULTS_FOLDER_PATH = current_dir + "/results/evaluations"
Path(RESULTS_FOLDER_PATH).mkdir(parents=True, exist_ok=True)


def parse_arguments() -> Dict[str, str]:
    parser = ArgumentParser()
    parser.add_argument(
        "--results-filename",
        required=True,
        help="File name to store the results",
    )
    parser.add_argument(
        "--experiment-names",
        nargs="+",
        required=True,
        help="Experiments to evaluate",
    )
    parser.add_argument(
        "--metrics",
        nargs="+",
        required=True,
        help="Number of metrics to calculate",
    )

    args = parser.parse_args()
    return args.__dict__


async def main():
    args = parse_arguments()
    results_filename = args["results_filename"]
    experiment_names = args["experiment_names"]
    metrics = args["metrics"]

    results_df = pd.DataFrame(columns=["experiment_name", *metrics])
    comparison_df = pd.DataFrame(columns=["docs", "gold_summaries", *experiment_names])

    number_of_entries_check = None

    for experiment_name in tqdm(experiment_names):
        summaries_csv = summaries_csv_filename_from(experiment_name)
        summaries_df = pd.read_csv(summaries_csv)
        docs = summaries_df["docs"].tolist()
        gold_summaries = summaries_df["gold_summaries"].tolist()
        if gold_summaries[0].startswith("[") and gold_summaries[0].endswith("]"):
            gold_summaries = [eval(summary) for summary in gold_summaries]
        else:
            gold_summaries = [[summary] for summary in gold_summaries]
        output_summaries = summaries_df["summaries"].tolist()
        comparison_df[experiment_name] = output_summaries

        if number_of_entries_check is not None:
            assert number_of_entries_check == len(output_summaries)
            assert comparison_df["docs"].tolist() == docs
        else:
            comparison_df["docs"] = docs
            comparison_df["gold_summaries"] = gold_summaries
            number_of_entries_check = len(output_summaries)

        metric2score = {}
        for metric in metrics:
            score = METRIC_2_CALCULATOR[SummarizationMetric(metric)].execute(
                documents=docs,
                gold_summaries=gold_summaries,
                output_summaries=output_summaries,
            )
            metric2score[metric] = score

        results_df = results_df.append(
            {"experiment_name": experiment_name, **metric2score}, ignore_index=True
        )

    comparison_df.to_csv(
        f"{RESULTS_FOLDER_PATH}/{results_filename}_comparison.csv", index=False
    )
    results_df.to_csv(
        f"{RESULTS_FOLDER_PATH}/{results_filename}_results.csv", index=False
    )


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
