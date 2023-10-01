import asyncio
import os
import time
from argparse import ArgumentParser
from typing import Dict

import pandas as pd

from tools.experimentation.metrics.bert_score import BertScoreMetricCalculator
from tools.experimentation.metrics.bleu import BleuMetricCalculator
from tools.experimentation.metrics.rouge import RougeMetricCalculator

SUMMARY_DIR = "./tools/experimentation/results/summaries/"
PER_SUMMARY_RESULTS_DIR = "./tools/experimentation/results/evaluations"


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
    a_summaries_csv = os.path.join(SUMMARY_DIR, method_a + ".csv")
    b_summaries_csv = os.path.join(SUMMARY_DIR, method_b + ".csv")

    rouge_1 = (
        RougeMetricCalculator(rouge_key="rouge1", exclude_stopwords=True)
        if "scitldr" in method_a
        else RougeMetricCalculator(rouge_key="rouge1")
    )
    rouge_2 = (
        RougeMetricCalculator(rouge_key="rouge2", exclude_stopwords=True)
        if "scitldr" in method_a
        else RougeMetricCalculator(rouge_key="rouge2")
    )
    rouge_l = (
        RougeMetricCalculator(rouge_key="rougeL", exclude_stopwords=True)
        if "scitldr" in method_a
        else RougeMetricCalculator(rouge_key="rougeL")
    )
    bleu = BleuMetricCalculator()
    bert_score = BertScoreMetricCalculator()

    a_summaries = pd.read_csv(a_summaries_csv)["summaries"].to_list()
    b_summaries = pd.read_csv(b_summaries_csv)["summaries"].to_list()
    gold_summaries = pd.read_csv(a_summaries_csv)["gold_summaries"].to_list()
    if gold_summaries[0].startswith("[") and gold_summaries[0].endswith("]"):
        gold_summaries = [eval(summary) for summary in gold_summaries]
    else:
        gold_summaries = [[summary] for summary in gold_summaries]

    a_rouge_1s = []
    a_rouge_2s = []
    a_rouge_ls = []
    a_bleus = []
    a_bert_scores = []
    b_rouge_1s = []
    b_rouge_2s = []
    b_rouge_ls = []
    b_bleus = []
    b_bert_scores = []

    for a_summary, b_summary, gold_summary in zip(
        a_summaries, b_summaries, gold_summaries
    ):
        a_rouge_1s.append(rouge_1.execute([], [gold_summary], [a_summary]))
        b_rouge_1s.append(rouge_1.execute([], [gold_summary], [b_summary]))
        a_rouge_2s.append(rouge_2.execute([], [gold_summary], [a_summary]))
        b_rouge_2s.append(rouge_2.execute([], [gold_summary], [b_summary]))
        a_rouge_ls.append(rouge_l.execute([], [gold_summary], [a_summary]))
        b_rouge_ls.append(rouge_l.execute([], [gold_summary], [b_summary]))
        a_bleus.append(bleu.execute([], [gold_summary], [a_summary]))
        b_bleus.append(bleu.execute([], [gold_summary], [b_summary]))
        a_bert_scores.append(bert_score.execute([], [gold_summary], [a_summary]))
        b_bert_scores.append(bert_score.execute([], [gold_summary], [b_summary]))

    results = pd.DataFrame(
        {
            "a_rouge_1s": a_rouge_1s,
            "b_rouge_1s": b_rouge_1s,
            "a_rouge_2s": a_rouge_2s,
            "b_rouge_2s": b_rouge_2s,
            "a_rouge_ls": a_rouge_ls,
            "b_rouge_ls": b_rouge_ls,
            "a_bleus": a_bleus,
            "b_bleus": b_bleus,
            "a_bert_scores": a_bert_scores,
            "b_bert_scores": b_bert_scores,
        }
    )
    results.to_csv(
        os.path.join(PER_SUMMARY_RESULTS_DIR, method_a + "_vs_" + method_b + ".csv")
    )


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
