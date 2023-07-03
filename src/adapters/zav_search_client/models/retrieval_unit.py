from enum import Enum


class RetrievalUnit(str, Enum):
    DOCUMENT = "document"
    CHUNK = "chunk"
    SENTENCE = "sentence"

    def __str__(self) -> str:
        return str(self.value)
