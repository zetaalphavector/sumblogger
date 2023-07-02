import enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from zav.message_bus import Command


@dataclass
class ExecuteTextCompletionSingleUsecase(Command):
    usecase: str
    variant: str
    prompt_params_list: List[Dict[str, Any]]
    params_mapping: Optional[Dict[str, str]] = None
    should_flatten: bool = False


class UsecaseCommandsExecutionType(enum.Enum):
    CHAIN = "chain"
    PARALLEL = "parallel"


@dataclass
class ExecuteTextCompletionUsecases(Command):
    usecase_commands: List[
        Union[ExecuteTextCompletionSingleUsecase, "ExecuteTextCompletionUsecases"]
    ]
    execution_type: UsecaseCommandsExecutionType
    prompt_params_list: Optional[List[Dict[str, Any]]] = None
    params_mapping: Optional[Dict[str, str]] = None
