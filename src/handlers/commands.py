from dataclasses import dataclass
from typing import Dict

from zav.message_bus import Command


@dataclass
class ExecuteTextCompletionUsecase(Command):
    usecase: str
    variant: str
    prompt_params: Dict[str, str]
