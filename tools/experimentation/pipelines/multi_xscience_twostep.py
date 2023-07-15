from src.handlers.commands import (
    ExecuteTextCompletionSingleUsecase,
    ExecuteTextCompletionUsecases,
    UsecaseCommandsExecutionType,
)
from tools.experimentation.datasets.multi_xscience import (
    average_words_count_per_summary,
    load_multi_xscience_dataset,
)
from tools.experimentation.datasets.types import FoldName
from tools.experimentation.pipelines import Experiment


class TwoStepMultiXScienceExperiment(Experiment):
    def load_dataset(self, offset: int = 0, size_limit: int = 100):
        self.dataset = load_multi_xscience_dataset(offset=offset, size_limit=size_limit)

    def build_command(self):
        dataset = self.dataset

        target_words_count = average_words_count_per_summary(
            self.dataset.fold_name2data[FoldName.TRAIN]
        )

        test_documents_list = dataset.fold_name2data[FoldName.TEST].documents_batches

        multi_doc_summary_commands = []
        for documents in test_documents_list:
            main_document = documents[0]
            ref_documents = [d.split(":", 1)[1] for d in documents[1:]]
            ref_document_ids = [d.split(":", 1)[0] for d in documents[1:]]
            command = ExecuteTextCompletionUsecases(
                execution_type=UsecaseCommandsExecutionType.CHAIN,
                prompt_params=None,
                usecase_commands=[
                    ExecuteTextCompletionUsecases(
                        execution_type=UsecaseCommandsExecutionType.PARALLEL,
                        prompt_params=None,
                        usecase_commands=[
                            ExecuteTextCompletionSingleUsecase(
                                usecase="single_doc_summary",
                                variant="multi_science_sds_step",
                                prompt_params={
                                    "main_document": main_document,
                                    "ref_document": ref_doc,
                                },
                                params_mapping={
                                    "summary": "ref_documents",
                                },
                            )
                            for ref_doc in ref_documents
                        ],
                    ),
                    ExecuteTextCompletionSingleUsecase(
                        usecase="multi_doc_summary",
                        variant="multi_xscience_mds_step",
                        prompt_params={
                            "main_document": main_document,
                            "ref_document_ids": ref_document_ids,
                            "number_of_words": target_words_count,
                        },
                        params_mapping={
                            "summary": "multi_doc_summary",
                        },
                    ),
                ],
            )

            multi_doc_summary_commands.append(command)

        return ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.PARALLEL,
            prompt_params=None,
            usecase_commands=multi_doc_summary_commands,
            params_mapping={
                "multi_doc_summary": "generated_summaries",
                "ref_documents": "single_doc_summaries",
                "main_document": "main_documents",
                "ref_document": "ref_documents",
            },
        )

    def get_gold_summaries(self):
        return self.dataset.fold_name2data[FoldName.TEST].gold_summaries

    def get_input_documents(self):
        return self.dataset.fold_name2data[FoldName.TEST].documents_batches
