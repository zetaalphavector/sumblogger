from enum import Enum


class DocumentSearchDocumentTypesItem(str, Enum):
    DOCUMENT = "document"
    CITATION = "citation"
    NOTE = "note"

    def __str__(self) -> str:
        return str(self.value)
