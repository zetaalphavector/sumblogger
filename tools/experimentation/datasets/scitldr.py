from typing import Optional

from datasets import load_dataset

from tools.experimentation.datasets.types import FoldName, SDSDataset, SDSDatasetFold


def average_words_count_per_summary(dataset_fold: SDSDatasetFold):
    if isinstance(dataset_fold.gold_summaries[0], list):
        words_counts = [
            len(summary.split()) for summary in dataset_fold.gold_summaries[0]
        ]
    else:
        words_counts = [
            len(summary.split()) for summary in dataset_fold.gold_summaries  # type: ignore
        ]

    avg_words_count = sum(words_counts) / len(words_counts)
    return int(avg_words_count)


def __create_fold(fold, size_limit: Optional[int] = None) -> SDSDatasetFold:
    return SDSDatasetFold(
        titles=None,
        documents=[" ".join(source) for source in fold["source"]][:size_limit],
        gold_summaries=fold["target"][:size_limit],
    )


def load_scitldr_dataset(offset=0, size_limit=100) -> SDSDataset:
    dataset = load_dataset("allenai/scitldr")

    test_fold = dataset["test"].select(range(offset, offset + size_limit))  # type: ignore
    return SDSDataset(
        fold_name2data={
            FoldName.TRAIN: __create_fold(dataset["train"]),  # type: ignore
            FoldName.VALID: __create_fold(dataset["validation"]),  # type: ignore
            FoldName.TEST: __create_fold(test_fold),  # type: ignore
        },
    )
