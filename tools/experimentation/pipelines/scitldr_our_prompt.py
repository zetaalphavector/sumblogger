from typing import List, Union

from responses import target

from src.handlers.commands import (
    ExecuteTextCompletionSingleUsecase,
    ExecuteTextCompletionUsecases,
    UsecaseCommandsExecutionType,
)
from tools.experimentation.datasets.scitldr import (
    average_words_count_per_summary,
    load_scitldr_dataset,
)
from tools.experimentation.datasets.types import FoldName
from tools.experimentation.pipelines import Experiment


class OurPromptSciTLDRExperiment(Experiment):
    def get_usecase_variant(self):
        raise NotImplementedError

    def load_dataset(self, offset: int = 0, size_limit: int = 100):
        self.dataset = load_scitldr_dataset(offset=offset, size_limit=size_limit)

    def build_command(self):
        dataset = self.dataset

        test_documents = dataset.fold_name2data[FoldName.TEST].documents

        target_words_count = average_words_count_per_summary(
            dataset_fold=dataset.fold_name2data[FoldName.TRAIN]
        )

        return ExecuteTextCompletionUsecases(
            execution_type=UsecaseCommandsExecutionType.PARALLEL,
            prompt_params=None,
            usecase_commands=[
                ExecuteTextCompletionSingleUsecase(
                    usecase="single_doc_summary",
                    variant=self.get_usecase_variant(),
                    prompt_params={
                        "document": document,
                        "number_of_words": target_words_count,
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


class OurZeroShotPromptSciTLDRExperiment(OurPromptSciTLDRExperiment):
    def get_usecase_variant(self):
        return "scitldr_zero_shot"


class OurTwoShotPromptSciTLDRExperiment(OurPromptSciTLDRExperiment):
    def get_usecase_variant(self):
        return "scitldr_two_shot"
