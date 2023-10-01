import asyncio
import os
import time
from argparse import ArgumentParser
from typing import Dict

import pandas as pd
from scipy.stats import ttest_rel

from tools.experimentation.metrics.bert_score import BertScoreMetricCalculator
from tools.experimentation.metrics.bleu import BleuMetricCalculator
from tools.experimentation.metrics.rouge import RougeMetricCalculator

PER_SUMMARY_RESULTS_DIR = "./tools/experimentation/results/evaluations"
PAIRED_TTEST_RESULTS_DIR = "./tools/experimentation/results/evaluations"

PAIRS = [
    ("rouge_1", "a_rouge_1s", "b_rouge_1s"),
    ("rouge_2", "a_rouge_2s", "b_rouge_2s"),
    ("rouge_l", "a_rouge_ls", "b_rouge_ls"),
    ("bleu", "a_bleus", "b_bleus"),
    ("bert_score", "a_bert_scores", "b_bert_scores"),
]


def parse_arguments() -> Dict[str, str]:
    parser = ArgumentParser()
    parser.add_argument(
        "--experiment-names",
        nargs=2,
        required=True,
        help="Experiments to evaluate",
    )

    args = parser.parse_args()
    return args.__dict__


async def main():
    args = parse_arguments()
    method_a, method_b = args["experiment_names"]
    per_summary_results_csv = os.path.join(
        PER_SUMMARY_RESULTS_DIR, method_a + "_vs_" + method_b + ".csv"
    )
    per_summary_df = pd.read_csv(per_summary_results_csv)

    ttest_results_txt = os.path.join(
        PAIRED_TTEST_RESULTS_DIR, method_a + "_vs_" + method_b + ".txt"
    )

    for name, col_a, col_b in PAIRS:
        a = per_summary_df[col_a].to_numpy()
        b = per_summary_df[col_b].to_numpy()
        t_statistic, p_value = ttest_rel(a, b)

        with open(ttest_results_txt, "a") as f:
            f.write(f"{name}: Paired t-test results:\n")
            f.write("t-statistic: " + str(t_statistic) + "\n")
            f.write("p-value: " + str(p_value) + "\n")
            f.write("Is it significant? " + str(p_value < 0.05) + "\n")
            f.write(50 * "-" + "\n")


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
