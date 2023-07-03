from enum import Enum


class DocumentSearchSortPopularity(str, Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
