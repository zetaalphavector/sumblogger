from typing import Any, Dict, List, Optional

from typing_extensions import NotRequired, TypedDict


class TextCompletionUsecaseForm(TypedDict):
    usecase: str
    variant: str
    prompt_params_list: List[Dict[str, Any]]
    params_mapping: NotRequired[Dict[str, str]]
    should_flatten: NotRequired[bool]


class TextCompletionUsecaseItem(TypedDict):
    output_params_list: List[Dict[str, Any]]


class TextCompletionChainForm(TypedDict):
    usecase_forms: List[TextCompletionUsecaseForm]


class TextCompletionChainItem(TypedDict):
    output_params_list: List[Dict[str, Any]]


class TextCompletionParallelForm(TypedDict):
    usecase_forms: List[TextCompletionUsecaseForm]


class TextCompletionParallelItem(TypedDict):
    usecase_items: List[TextCompletionUsecaseItem]
