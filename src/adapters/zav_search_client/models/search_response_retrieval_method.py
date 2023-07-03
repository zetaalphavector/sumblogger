from enum import Enum


class SearchResponseRetrievalMethod(str, Enum):
    KEYWORD = "keyword"
    KNN = "knn"

    def __str__(self) -> str:
        return str(self.value)
