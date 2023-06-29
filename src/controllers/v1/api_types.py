from typing import Any, Dict, List, Union

from typing_extensions import NotRequired, TypedDict


class TextCompletionSingleUsecaseForm(TypedDict):
    usecase: str
    variant: str
    prompt_params_list: List[Dict[str, Any]]
    params_mapping: NotRequired[Dict[str, str]]
    should_flatten: NotRequired[bool]


class TextCompletionUsecaseItem(TypedDict):
    output_params_list: List[Dict[str, Any]]


class TextCompletionChainForm(TypedDict):
    chain_usecase_forms: List[TextCompletionSingleUsecaseForm]


TextCompletionChainItem = TextCompletionUsecaseItem


class TextCompletionParallelForm(TypedDict):
    parallel_usecase_forms: List[
        Union[TextCompletionSingleUsecaseForm, TextCompletionChainForm]
    ]
    should_flatten: NotRequired[bool]


class TextCompletionParallelItem(TypedDict):
    usecase_items: List[TextCompletionUsecaseItem]
