from typing import Optional

from datasets import load_dataset

from tools.experimentation.datasets.types import FoldName, MDSDataset, MDSDatasetFold


def average_words_count_per_summary(dataset_fold: MDSDatasetFold):
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


def __documents_from(main_doc, ref_docs):
    # docs = [main_doc] + ref_docs["abstract"]
    docs = [main_doc] + [
        f"{cite_index}:{abstract}"
        for cite_index, abstract in zip(ref_docs["cite_N"], ref_docs["abstract"])
    ]
    return [doc for doc in docs if doc != ""]


def __create_fold(fold, size_limit: Optional[int] = None) -> MDSDatasetFold:
    return MDSDatasetFold(
        titles=None,
        documents_batches=[
            __documents_from(main_doc, ref_docs)
            for main_doc, ref_docs in zip(
                fold[:size_limit]["abstract"], fold[:size_limit]["ref_abstract"]
            )
        ],
        gold_summaries=fold["related_work"][:size_limit],
    )


def load_multi_xscience_dataset(offset=0, size_limit=100) -> MDSDataset:

    dataset = load_dataset("multi_x_science_sum")

    test_fold = dataset["test"].select(range(offset, offset + size_limit))  # type: ignore

    return MDSDataset(
        fold_name2data={
            FoldName.TRAIN: __create_fold(dataset["train"]),  # type: ignore
            FoldName.VALID: __create_fold(dataset["validation"]),  # type: ignore
            FoldName.TEST: __create_fold(test_fold),
        },
    )
