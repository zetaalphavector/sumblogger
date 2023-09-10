from collections import defaultdict
from typing import Dict, List

from fastapi import APIRouter
from zav.api.errors import NotFoundException

from src.controllers.v1.api_types import (
    DocumentsClustersSummariesOutputParams,
    VosBlogpostOutputParams,
)
from src.types.documents import DocumentsCluster
from src.types.vos import (
    Cluster,
    ClusterColor,
    ColorSchemes,
    Item,
    Link,
    Summary,
    VosClusteredDocuments,
    VosConferenceClusteredDocuments,
    VosNetwork,
)

SINGLE_VOS_CLUSTER_ID = 1
SINGLE_VOS_REPRESENTATICE_DOCS_CLUSTER_ID = 2
RED_COLOR = "#d62728"
CLUSTER_COLORS_PALLETTE = [
    "#2ca02c",
    "#1f77b4",
    "#bcbd22",
    "#9467bd",
    "#17becf",
    "#ff7f0e",
    "#8c564b",
    "#e377c2",
    "#ff9896",
    "#98df8a",
    "#aec7e8",
    "#dbdb8d",
    "#c5b0d5",
    "#9edae5",
    "#ffbb78",
    "#c49c94",
    "#f7b6d2",
]


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
    summaries_item_params: DocumentsClustersSummariesOutputParams,
    vos_clustered_documents_request: VosConferenceClusteredDocuments,
) -> VosConferenceClusteredDocuments:
    output_params = summaries_item_params
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


def to_vos_blogpost_response(
    blogpost_item_params: VosBlogpostOutputParams,
    vos_clustered_documents_request: VosConferenceClusteredDocuments,
) -> VosConferenceClusteredDocuments:

    vos = to_vos_clustered_documents_response(
        blogpost_item_params, vos_clustered_documents_request
    )

    vos.network.blog_title = blogpost_item_params["blog_title"]
    vos.network.blog_intro = blogpost_item_params["blog_intro"]
    vos.network.blog_conclusion = blogpost_item_params["blog_conclusion"]

    if vos.network.clusters is None:
        raise NotFoundException("No clusters found")

    for i, cluster in enumerate(vos.network.clusters):
        cluster.label = blogpost_item_params["cluster_titles"][i]

    return vos


vos_conference_summaries_router = APIRouter(tags=["vos_conference_summaries"])


def __vos_with_adapted_colors(
    vos: VosConferenceClusteredDocuments,
) -> VosConferenceClusteredDocuments:
    color_adapted_vos = vos.copy(deep=True)

    if color_adapted_vos.network.clusters is None:
        raise ValueError("Clusters are not defined in the VOS network")

    color_adapted_vos.config.color_schemes = ColorSchemes(
        cluster_colors=[
            ClusterColor(
                cluster=cluster.cluster,
                color=CLUSTER_COLORS_PALLETTE[cluster.cluster - 1],
            )
            for cluster in color_adapted_vos.network.clusters
        ]
    )
    return color_adapted_vos


def cluster2vos_from(
    vos: VosConferenceClusteredDocuments,
    highlight_nodes_with_summaries: bool,
) -> Dict[int, VosClusteredDocuments]:

    input_vos = __vos_with_adapted_colors(vos)
    vos = input_vos.copy(deep=True)
    if vos.network.clusters is None:
        raise ValueError("Clusters are not defined in the VOS network")

    cluster2vos = defaultdict()
    for cluster in vos.network.clusters:
        cluster_items = items_from(cluster.cluster, vos.network.items)
        cluster_links = links_between(cluster_items, vos.network.links)

        for item in cluster_items:
            if item.summary is not None and highlight_nodes_with_summaries:
                item.cluster = SINGLE_VOS_REPRESENTATICE_DOCS_CLUSTER_ID
            else:
                item.cluster = SINGLE_VOS_CLUSTER_ID

        config = vos.config.copy(deep=True)
        config.parameters.max_n_links = 1000

        single_cluster_vos = VosClusteredDocuments(
            config=config,
            network=VosNetwork(
                items=cluster_items,
                links=cluster_links,
                clusters=[
                    Cluster(cluster=SINGLE_VOS_CLUSTER_ID, label=cluster.label),
                    Cluster(
                        cluster=SINGLE_VOS_REPRESENTATICE_DOCS_CLUSTER_ID,
                        label="Representative documents of cluster",
                    ),
                ],
            ),
        )
        single_cluster_vos.config.color_schemes = ColorSchemes(
            cluster_colors=[
                ClusterColor(
                    cluster=SINGLE_VOS_CLUSTER_ID,
                    color=CLUSTER_COLORS_PALLETTE[cluster.cluster - 1],
                ),
                ClusterColor(
                    cluster=SINGLE_VOS_REPRESENTATICE_DOCS_CLUSTER_ID,
                    color=RED_COLOR,
                ),
            ]
        )
        cluster2vos[cluster.cluster] = single_cluster_vos

    return cluster2vos


def items_from(cluster_id: int, items: List[Item]) -> List[Item]:
    return [
        item.copy(deep=True)
        for item in items
        if item.cluster == cluster_id and "cluster_" not in item.id
    ]


def links_between(items: List[Item], total_links: List[Link]) -> List[Link]:
    item_ids = [item.id for item in items]
    return [
        link.copy(deep=True)
        for link in total_links
        if link.source_id in item_ids and link.target_id in item_ids
        # and link.strength > 0.5
    ]
