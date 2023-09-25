from typing import List, Union

from src.handlers.commands import (
    ExecuteTextCompletionSingleUsecase,
    ExecuteTextCompletionUsecases,
    UsecaseCommandsExecutionType,
)
from tools.experimentation.datasets.scitldr import load_scitldr_dataset
from tools.experimentation.datasets.types import FoldName
from tools.experimentation.pipelines import Experiment


class VanillaSciTLDRExperiment(Experiment):
    def load_dataset(self, offset: int = 0, size_limit: int = 100):
        self.dataset = load_scitldr_dataset(offset=offset, size_limit=size_limit)

    def build_command(self):
        dataset = self.dataset

        test_documents = dataset.fold_name2data[FoldName.TEST].documents

        return ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.PARALLEL,
            prompt_params=None,
            usecase_commands=[
                ExecuteTextCompletionSingleUsecase(
                    usecase="single_doc_summary",
                    variant="scitldr_vanilla",
                    prompt_params={
                        "document": document,
                    },
                    params_mapping={
                        "summary": "generated_summaries",
                    },
                )
                for document in test_documents
            ],
        )

    def get_gold_summaries(self) -> Union[List[str], List[List[str]]]:
        return self.dataset.fold_name2data[FoldName.TEST].gold_summaries

    def get_input_documents(self):
        return self.dataset.fold_name2data[FoldName.TEST].documents
