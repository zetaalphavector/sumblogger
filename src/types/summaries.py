from typing import Dict, Optional, TypedDict

from src.types.documents import Document, DocumentsCluster, Topic


class ContentSummary(TypedDict):
    content: str
    topic: Optional[Topic]
    long: Optional[str]
    tldr: str


DocumentPartSummary = ContentSummary
DocumentSummary = ContentSummary
ClusterSummary = ContentSummary


Document2Summary = Dict[Document, DocumentSummary]
DocumentId2Summary = Dict[str, DocumentSummary]
Cluster2Summary = Dict[DocumentsCluster, ClusterSummary]
ClusterId2Summary = Dict[str, ClusterSummary]

Cluster2Document2Summary = Dict[DocumentsCluster, Document2Summary]
ClusterId2DocumentId2Summary = Dict[str, DocumentId2Summary]


class Contents2Summaries(TypedDict):
    cluster2summary: ClusterId2Summary
    cluster2document2summary: Optional[ClusterId2DocumentId2Summary]
