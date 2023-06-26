from typing import Dict

from typing_extensions import TypedDict


class TextCompletionUsecaseForm(TypedDict):
    usecase: str
    variant: str
    prompt_params: Dict[str, str]


class TextCompletionUsecaseItem(TypedDict):
    response: str
