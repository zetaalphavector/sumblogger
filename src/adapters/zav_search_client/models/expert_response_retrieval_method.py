from enum import Enum


class ExpertResponseRetrievalMethod(str, Enum):
    KEYWORD = "keyword"
    KNN = "knn"

    def __str__(self) -> str:
        return str(self.value)
