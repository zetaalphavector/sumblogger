from typing import Dict, List

from zav.logging import logger
from zav.message_bus import EventHandlerRegistry  # noqa F401
from zav.message_bus import CommandHandlerRegistry, Message

from src.handlers import commands
from src.services.retrieval.retrieve_documents import RetrieveDocumentsService
from src.types.documents import Document, DocumentsCluster
from src.types.exceptions import NotFoundException
from src.types.vos import VosNetwork


@CommandHandlerRegistry.register(commands.BuildDocumentsClusters)
async def build_docs_clusters(
    cmd: commands.BuildDocumentsClusters,
    queue: List[Message],
    retrieve_docs_service: RetrieveDocumentsService,
) -> Dict[str, DocumentsCluster]:
    return await __to_documents_cluster(
        cmd.vos_network,
        retrieve_docs_service,
    )


def __id_from(guid: str) -> str:
    return guid.split("_")[0]


async def __to_documents_cluster(
    vos_network: VosNetwork,
    retrieve_documents_service: RetrieveDocumentsService,
) -> Dict[str, DocumentsCluster]:
    items = [item for item in vos_network.items if item.type != "ClusterLabel"]

    doc_ids = [__id_from(item.id) for item in items]
    retrieved_documents = await retrieve_documents_service.get_by_ids(doc_ids)

    if retrieved_documents is None:
        raise NotFoundException("Could not find abstracts for the given ids")

    docid2abstract = {
        __id_from(doc["id"]): doc["abstract"] for doc in retrieved_documents
    }
    docid2year = {__id_from(doc["id"]): doc["year"] for doc in retrieved_documents}
    docid2created_at = {
        __id_from(doc["id"]): doc["created_at"] for doc in retrieved_documents
    }

    for id in doc_ids:
        if id not in docid2abstract:
            logger.warn(f"Could not find abstract for guid: {id}")
            # raise NotFoundException(f"Could not find abstract for guid: {id}")

    return {
        str(cluster_id): DocumentsCluster(
            cluster_id=str(cluster_id),
            guid2document={
                item.id: Document(
                    id=item.id,
                    title=item.title,
                    abstract=docid2abstract[__id_from(item.id)],
                    content=docid2abstract[__id_from(item.id)],
                    url=item.uri or "",
                    authors=item.authors.split(", ") if item.authors else [],
                    year=docid2year[__id_from(item.id)],
                    created_at=docid2created_at[__id_from(item.id)],
                )
                for item in items
                if item.cluster == cluster_id
            },
        )
        for cluster_id in {
            item.cluster
            for item in vos_network.items
            if __id_from(item.id) in docid2abstract
        }
    }
