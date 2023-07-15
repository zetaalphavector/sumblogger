from typing import Dict

from src.handlers.commands import (
    ExecuteTextCompletionSingleUsecase,
    ExecuteTextCompletionUsecases,
    UsecaseCommandsExecutionType,
)
from src.types.documents import DocumentsCluster


def build_usecases_command(
    id2documents_clusters: Dict[str, DocumentsCluster],
    intro_paragraph_words_count: int,
    summary_paragraph_words_count: int,
    detailed_paragraph_usecase_variant: str = "oneshot_detailed_paragraph",
) -> ExecuteTextCompletionUsecases:
    cluster_id2usecases_cmd = {}
    for cluster_id, cluster in id2documents_clusters.items():
        documents = list(cluster["guid2document"].values())[:100]
        single_doc_summary_usecases = __single_doc_usecase_for(documents)

        multi_doc_summary_usecases = __multi_doc_summary_usecases_for(
            intro_paragraph_words_count,
            summary_paragraph_words_count,
            detailed_paragraph_usecase_variant,
        )

        usecases_cmd = ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            prompt_params={"cluster_id": cluster_id},
            usecase_commands=[
                single_doc_summary_usecases,
                multi_doc_summary_usecases,
            ],
        )
        cluster_id2usecases_cmd[cluster_id] = usecases_cmd

    return ExecuteTextCompletionUsecases(
        execution_type=UsecaseCommandsExecutionType.PARALLEL,
        usecase_commands=list(cluster_id2usecases_cmd.values()),
        params_mapping={
            "intro_paragraph": "intro_paragraphs",
            "detailed_paragraph": "detailed_paragraphs",
            "documents": "single_doc_summaries",
            "cluster_id": "cluster_ids",
            "doc_id": "doc_ids",
        },
    )


def __multi_doc_summary_usecases_for(
    intro_paragraph_words_count,
    summary_paragraph_words_count,
    detailed_paragraph_usecase_variant,
):
    intro_multi_doc_usecase = ExecuteTextCompletionSingleUsecase(
        usecase="multi_doc_summary",
        variant="oneshot_intro_paragraph",
        prompt_params={"number_of_words": intro_paragraph_words_count, "retries": 3},
        params_mapping={"summary": "intro_paragraph"},
    )
    summary_multi_doc_usecase = ExecuteTextCompletionSingleUsecase(
        usecase="multi_doc_summary",
        variant=detailed_paragraph_usecase_variant,
        prompt_params={"number_of_words": summary_paragraph_words_count, "retries": 3},
        params_mapping={"summary": "detailed_paragraph"},
    )
    return ExecuteTextCompletionUsecases(
        execution_type=UsecaseCommandsExecutionType.PARALLEL,
        usecase_commands=[
            intro_multi_doc_usecase,
            summary_multi_doc_usecase,
        ],
    )


def __single_doc_usecase_for(documents):
    return ExecuteTextCompletionUsecases(
        execution_type=UsecaseCommandsExecutionType.PARALLEL,
        params_mapping={"summary": "documents", "doc_id": "doc_ids"},
        usecase_commands=[
            ExecuteTextCompletionSingleUsecase(
                usecase="single_doc_summary",
                variant="tldr",
                prompt_params={
                    "document": document["content"],
                    "number_of_words": 20,
                    "doc_id": doc_index,
                },
            )
            for doc_index, document in enumerate(documents)
        ],
    )
