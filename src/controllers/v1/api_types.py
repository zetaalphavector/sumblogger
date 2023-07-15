import enum
from typing import Any, Dict, List, Union

from typing_extensions import NotRequired, TypedDict


class TextCompletionSingleUsecaseForm(TypedDict):
    usecase: str
    variant: str
    prompt_params: Dict[str, Any]
    params_mapping: NotRequired[Dict[str, str]]


class UsecasesExecutionType(enum.Enum):
    CHAIN = "chain"
    PARALLEL = "parallel"


class TextCompletionUsecasesFormBase(TypedDict):
    prompt_params: Dict[str, Any]
    # usecase_forms should be
    # List[Union[TextCompletionSingleUsecaseForm, "TextCompletionUsecasesForm"]]
    # but mypy doesn't allow it
    usecase_forms: List[Any]
    execution_type: UsecasesExecutionType


class TextCompletionUsecasesForm(TypedDict):
    prompt_params: Dict[str, Any]
    usecase_forms: List[
        Union[TextCompletionSingleUsecaseForm, "TextCompletionUsecasesForm"]
    ]
    execution_type: UsecasesExecutionType


class TextCompletionUsecasesItem(TypedDict):
    output_params: Dict[str, Any]


class DocumentsClustersSummariesOutputParams(TypedDict):
    intro_paragraphs: List[str]
    detailed_paragraphs: List[str]
    single_doc_summaries: List[List[str]]
    cluster_ids: List[str]
    doc_ids: List[List[str]]


class DocumentsClustersSummariesItem(TypedDict):
    output_params: DocumentsClustersSummariesOutputParams
