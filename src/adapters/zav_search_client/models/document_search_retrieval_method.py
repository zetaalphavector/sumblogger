from enum import Enum


class DocumentSearchRetrievalMethod(str, Enum):
    KNN = "knn"
    KEYWORD = "keyword"

    def __str__(self) -> str:
        return str(self.value)
