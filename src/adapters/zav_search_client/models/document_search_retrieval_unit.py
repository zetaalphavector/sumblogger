from enum import Enum


class DocumentSearchRetrievalUnit(str, Enum):
    DOCUMENT = "document"
    CHUNK = "chunk"
    SENTENCE = "sentence"

    def __str__(self) -> str:
        return str(self.value)
