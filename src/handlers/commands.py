import enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from zav.message_bus import Command

from src.types.documents import DocumentsCluster
from src.types.vos import VosNetwork


@dataclass
class ExecuteTextCompletionSingleUsecase(Command):
    usecase: str
    variant: str
    prompt_params: Dict[str, Any]
    params_mapping: Optional[Dict[str, str]] = None


class UsecaseCommandsExecutionType(enum.Enum):
    CHAIN = "chain"
    PARALLEL = "parallel"


@dataclass
class ExecuteTextCompletionUsecases(Command):
    usecase_commands: List[
        Union[ExecuteTextCompletionSingleUsecase, "ExecuteTextCompletionUsecases"]
    ]
    execution_type: UsecaseCommandsExecutionType
    prompt_params: Optional[Dict[str, Any]] = None
    params_mapping: Optional[Dict[str, str]] = None


@dataclass
class BuildDocumentsClusters(Command):
    vos_network: VosNetwork


@dataclass
class SelectVosRepresentativeDocuments(Command):
    vos_network: VosNetwork
    top_k: int = 5


class SummarizeDocumentsClusters(Command):
    id2cluster: Dict[str, DocumentsCluster]
    intro_target_number_of_words: int = 30
    summary_target_number_of_words: int = 100
