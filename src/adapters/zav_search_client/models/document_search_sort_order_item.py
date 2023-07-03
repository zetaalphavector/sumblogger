from enum import Enum


class DocumentSearchSortOrderItem(str, Enum):
    DATE = "date"
    CITATIONS = "citations"
    SOURCE = "source"
    YEAR = "year"
    AUTHORITY = "authority"
    POPULARITY = "popularity"
    CODE = "code"

    def __str__(self) -> str:
        return str(self.value)
