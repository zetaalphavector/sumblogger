from typing import Dict, List

from zav.api.errors import NotFoundException
from zav.logging import logger

from src.controllers.v1.api_types import DocumentsClustersSummariesItem
from src.services.retrieval.retrieve_documents import RetrieveDocumentsService
from src.types.documents import Document, DocumentsCluster
from src.types.vos import Cluster, Summary, VosClusteredDocuments, VosNetwork


def id_from(guid: str) -> str:
    return guid.split("_")[0]


def cluster_from_id(
    cluster_id: str,
    documents_clusters: List[DocumentsCluster],
) -> DocumentsCluster:
    for cluster in documents_clusters:
        if cluster["cluster_id"] == cluster_id:
            return cluster

    raise NotFoundException(f"Could not find cluster with id: {cluster_id}")


def to_vos_clustered_documents_response(
    summaries_item: DocumentsClustersSummariesItem,
    vos_clustered_documents_request: VosClusteredDocuments,
) -> VosClusteredDocuments:
    output_params = summaries_item["output_params"]
    print(f"output_params: {output_params}")
    if vos_clustered_documents_request.network.clusters is None:
        return vos_clustered_documents_request

    cluster_id2doc_id2summary = {}
    for cluster_id, summaries, doc_ids in zip(
        output_params["cluster_ids"],
        output_params["single_doc_summaries"],
        output_params["doc_ids"],
    ):
        cluster_id2doc_id2summary[cluster_id] = {}
        for doc_id, summary in zip(doc_ids, summaries):
            cluster_id2doc_id2summary[cluster_id][doc_id] = summary

    response = vos_clustered_documents_request
    for item in response.network.items:
        if item.id in cluster_id2doc_id2summary[str(item.cluster)]:
            item.summary = Summary(
                tldr_summary=cluster_id2doc_id2summary[str(item.cluster)][item.id]
            )

    vos_clusters = []
    for cluster_ids, intro_paragraph, detailed_summary in zip(
        output_params["cluster_ids"],
        output_params["intro_paragraphs"],
        output_params["detailed_paragraphs"],
    ):
        cluster_id = cluster_ids[0]
        vos_clusters.append(
            Cluster(
                cluster=int(cluster_id),
                label=cluster_id,
                summary=Summary(
                    tldr_summary=intro_paragraph + "\n\n" + detailed_summary,
                ),
            )
        )

    response.network.clusters = vos_clusters

    return response
