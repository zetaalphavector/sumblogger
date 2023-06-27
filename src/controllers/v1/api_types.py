from typing import Dict, List, Optional

from typing_extensions import NotRequired, TypedDict


class TextCompletionUsecaseForm(TypedDict):
    usecase: str
    variant: str
    prompt_params_list: List[Dict[str, str]]
    params_mapping: NotRequired[Dict[str, str]]


class TextCompletionUsecaseItem(TypedDict):
    output_params: List[Dict[str, str]]
