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


class OneStepMultiXScienceExperiment(Experiment):
    def load_dataset(self, offset: int = 0, size_limit: int = 100):
        self.dataset = load_multi_xscience_dataset(offset=offset, size_limit=size_limit)

    def build_command(self):
        dataset = self.dataset

        target_words_count = average_words_count_per_summary(
            dataset.fold_name2data[FoldName.TRAIN]
        )

        test_documents_list = dataset.fold_name2data[FoldName.TEST].documents_batches

        return ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.CHAIN,
            prompt_params_list=None,
            usecase_commands=[
                ExecuteTextCompletionSingleUsecase(
                    usecase="multi_doc_summary",
                    variant="multi_xscience_one_step",
                    prompt_params_list=[
                        {
                            "main_document": documents[0],
                            "ref_documents": [
                                d.split(":", 1)[1] for d in documents[1:]
                            ],
                            "ref_document_ids": [
                                d.split(":", 1)[0] for d in documents[1:]
                            ],
                            "number_of_words": target_words_count,
                        }
                        for documents in test_documents_list
                    ],
                    params_mapping={
                        "summary": "generated_summaries",
                    },
                    should_flatten=True,
                )
            ],
        )

    def get_gold_summaries(self):
        return self.dataset.fold_name2data[FoldName.TEST].gold_summaries

    def get_input_documents(self):
        return self.dataset.fold_name2data[FoldName.TEST].documents_batches
