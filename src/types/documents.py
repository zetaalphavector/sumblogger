from typing import Dict, List, Optional, TypedDict, Union


class Document(TypedDict):
    id: str
    title: str
    abstract: str
    content: str
    url: str
    authors: List[str]
    year: Optional[int]
    created_at: Optional[str]


class EmbeddedDocument(Document):
    embedding_id: str
    embedding: List[float]


class DocumentsCluster(TypedDict):
    cluster_id: str
    guid2document: Dict[str, Union[Document, EmbeddedDocument]]


class Topic(TypedDict):
    keywords: List[str]
    description: str


DocumentId2Topic = Dict[str, Topic]
ClusterId2DocumentId2Topic = Dict[str, DocumentId2Topic]
ClusterId2Topic = Dict[str, Topic]
