from enum import Enum


class PrivateDocStatusCode(str, Enum):
    PD001 = "PD001"
    PD002 = "PD002"

    def __str__(self) -> str:
        return str(self.value)
