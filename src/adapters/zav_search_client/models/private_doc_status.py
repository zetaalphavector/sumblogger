from enum import Enum


class PrivateDocStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)
