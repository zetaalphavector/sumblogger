from dataclasses import dataclass
from typing import Dict, List, Optional

from zav.message_bus import Command


@dataclass
class ExecuteTextCompletionUsecase(Command):
    usecase: str
    variant: str
    prompt_params_list: List[Dict[str, str]]
    params_mapping: Optional[Dict[str, str]] = None
