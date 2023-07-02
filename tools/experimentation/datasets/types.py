import dataclasses
import enum
from typing import Dict, List, Optional, Union


@dataclasses.dataclass
class MDSDatasetFold:
    titles: Optional[List[List[str]]]
    documents_batches: List[List[str]]
    gold_summaries: List[str]


class FoldName(enum.Enum):
    TRAIN = "train"
    VALID = "validation"
    TEST = "test"


@dataclasses.dataclass
class MDSDataset:
    fold_name2data: Dict[FoldName, MDSDatasetFold]


class MDSDatasetName(enum.Enum):
    Multi_XScience = "Multi_XScience"


@dataclasses.dataclass
class SDSDatasetFold:
    titles: Optional[List[str]]
    documents: List[str]
    gold_summaries: Union[List[List[str]], List[str]]


@dataclasses.dataclass
class SDSDataset:
    fold_name2data: Dict[FoldName, SDSDatasetFold]


class SDSDatasetName(enum.Enum):
    SciTLDR = "SciTLDR"
