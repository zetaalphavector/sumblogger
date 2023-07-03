from enum import Enum


class DocumentSearchCollapse(str, Enum):
    UID = "uid"

    def __str__(self) -> str:
        return str(self.value)
