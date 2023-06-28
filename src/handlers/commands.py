from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from zav.message_bus import Command


@dataclass
class ExecuteTextCompletionUsecase(Command):
    usecase: str
    variant: str
    prompt_params_list: List[Dict[str, Any]]
    params_mapping: Optional[Dict[str, str]] = None
    should_flatten: bool = False


@dataclass
class ExecuteTextCompletionChain(Command):
    usecase_commands: List[ExecuteTextCompletionUsecase]
