from typing import Any, Dict, List

from typing_extensions import NotRequired, TypedDict


class TextCompletionUsecaseForm(TypedDict):
    usecase: str
    variant: str
    prompt_params_list: List[Dict[str, str]]
    params_mapping: NotRequired[Dict[str, str]]
    should_flatten: NotRequired[bool]


class TextCompletionUsecaseItem(TypedDict):
    output_params_list: List[Dict[str, Any]]
