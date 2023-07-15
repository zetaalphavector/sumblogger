from datetime import datetime
from typing import Dict, List

from numpy import exp
from zav.logging import logger
from zav.message_bus import CommandHandlerRegistry, Message

from src.handlers import commands
from src.types.vos import Item, Link, VosNetwork, Weights

FAVOR_COVERAGE_WEIGHT = 1.0


@CommandHandlerRegistry.register(commands.SelectVosRepresentativeDocuments)
async def handle_setect_representative_docs(
    cmd: commands.SelectVosRepresentativeDocuments,
    queue: List[Message],
) -> VosNetwork:
    cluster_id2representative_item_ids = __representative_item_ids_per_cluster(
        cmd.vos_network, cmd.top_k
    )
    __log_stats(cluster_id2representative_item_ids, cmd.vos_network)

    all_representative_items = __items_from_ids(
        __flattened_item_ids_from(cluster_id2representative_item_ids),
        cmd.vos_network.items,
    )

    return __vos_network_from(all_representative_items, cmd.vos_network)


def __representative_item_ids_per_cluster(
    vos_network: VosNetwork,
    top_k: int,
) -> Dict[int, List[str]]:
    cluster_ids = {item.cluster for item in vos_network.items}

    cluster_id2selected_items_ids: Dict[int, List[str]] = {}

    # TODO: For performance improvement, we can parallelize across clusters
    for cluster_id in cluster_ids:
        cluster_items = __items_from(cluster_id, vos_network.items)
        cluster_links = __links_between(cluster_items, vos_network.links)

        cluster_item_id2links = {
            item.id: __links_of([item], cluster_links) for item in cluster_items
        }
        cluster_id2selected_items_ids[cluster_id] = __most_representative_items(
            cluster_items, cluster_item_id2links, top_k
        )
    return cluster_id2selected_items_ids


# def __most_representative_items(
#     cluster_items: List[Item],
#     cluster_item_id2links: Dict[str, List[Link]],
#     top_k: int,
# ) -> List[str]:
#     cluster_items = measure_impact_scores(normalize_weights(cluster_items))

#     item_id2similarity_score = measure_similarity_scores(
#         cluster_items,
#         cluster_item_id2links,
#     )

#     return sorted(
#         item_id2similarity_score,
#         key=lambda x: item_id2similarity_score[x],
#         reverse=True,
#     )[:top_k]


def __most_representative_items(
    cluster_items: List[Item],
    cluster_item_id2links: Dict[str, List[Link]],
    top_k: int,
):
    cluster_items = __measure_impact_scores(__normalize_weights(cluster_items))
    all_cluster_items_size = len(cluster_items)
    selected_items_ids = []
    represented_item_ids = set()
    # TODO: For performance improvement, we can use a max heap to get the top_k items
    while (
        top_k > 0
        and len(cluster_items) > 0
        # and len(represented_item_ids) < all_cluster_items_size
    ):
        top_k -= 1
        item_id2similarity_score = __measure_similarity_scores(
            cluster_items,
            cluster_item_id2links,
        )
        item_id2score = __interpolate_impact_and_similarity_scores(
            cluster_items, item_id2similarity_score
        )

        selected_item_id = max(item_id2score, key=lambda x: item_id2score[x])
        selected_items_ids.append(selected_item_id)

        represented_item_ids.update(
            __item_and_neigbors_of(selected_item_id, cluster_item_id2links)
        )
        cluster_items = __remove_selected_item(cluster_items, selected_item_id)
        __remove_redundant_links(cluster_item_id2links, selected_item_id)

    return selected_items_ids


def __normalize_weights(cluster_items: List[Item]) -> List[Item]:
    max_influence = max(item.weights.Influence for item in cluster_items)
    max_citations = max(item.weights.Citations for item in cluster_items)
    max_popularity = max(item.weights.Popularity for item in cluster_items)
    max_relevance = max(item.weights.Relevance for item in cluster_items)

    for item in cluster_items:
        item.normalized_w = Weights(
            Influence=item.weights.Influence / max_influence,
            Citations=item.weights.Citations / max_citations,
            Popularity=item.weights.Popularity / max_popularity,
            Relevance=item.weights.Relevance / max_relevance,
        )

    return cluster_items


def __measure_impact_scores(cluster_items: List[Item]) -> List[Item]:
    now = datetime.now()
    for item in cluster_items:
        date = datetime.strptime(item.heading.split(",")[-1].strip(), "%d %b %Y")
        age = (now - date).days
        if item.normalized_w is None:
            raise ValueError("Item has no normalized weights")

        item.impact_score = __impact_score_from(item.normalized_w, age)
    return cluster_items


def __impact_score_from(weights: Weights, age, exp_interpolation=0.0025):
    alpha = exp(-exp_interpolation * age)
    return (
        alpha * ((weights.Influence + weights.Popularity) / 2)
        + (1 - alpha) * weights.Citations
    )


def __remove_selected_item(cluster_items, selected_item_id):
    return [item for item in cluster_items if item.id != selected_item_id]


def __remove_redundant_links(cluster_item_id2links, selected_item_id):
    """
    Update the cluster_item_id2links by removing all links between either the
    selected item and its neighbors or between items that are neighbors of
    the selected item.

    That is because we assume that the selected item and its neighbors are already
    well represented by the selected item itself. Thus, we do not want to take these
    links into account anymore, since the nodes that they connect are already
    represented.


    Args:
        cluster_item_id2links (Dict[str, List[Link]])
        selected_item_id (str)
    """
    item_and_neighbor_ids = __item_and_neigbors_of(
        selected_item_id,
        cluster_item_id2links,
    )

    for item_id in item_and_neighbor_ids:
        links = []
        for link in cluster_item_id2links[item_id]:
            if (
                link.source_id not in item_and_neighbor_ids
                or link.target_id not in item_and_neighbor_ids
            ):
                links.append(link)
        cluster_item_id2links[item_id] = links

    cluster_item_id2links.pop(selected_item_id)


def __item_and_neigbors_of(selected_item_id, cluster_item_id2links):
    item_and_neighbor_ids = set()
    for link in cluster_item_id2links[selected_item_id]:
        item_and_neighbor_ids.add(link.source_id)
        item_and_neighbor_ids.add(link.target_id)
    return item_and_neighbor_ids


def __measure_similarity_scores(
    cluster_items, cluster_item_id2links
) -> Dict[str, float]:
    item_id2similarity_score = {}
    max_similarity_score = 0
    for item in cluster_items:
        similarity_score = __cumulative_strength_of(cluster_item_id2links[item.id])
        item_id2similarity_score[item.id] = similarity_score
        max_similarity_score = max(max_similarity_score, similarity_score)
    if max_similarity_score != 0.0:
        for item in cluster_items:
            item_id2similarity_score[item.id] /= max_similarity_score
    return item_id2similarity_score


def __interpolate_impact_and_similarity_scores(
    cluster_items: List[Item], item_id2similarity_score: Dict[str, float]
) -> Dict[str, float]:
    item_id2score = {}
    for item in cluster_items:
        item_id2score[item.id] = __item_score_from(
            item_id2similarity_score[item.id], item.impact_score
        )
    return item_id2score


def __item_score_from(
    similarity_score,
    impact_score,
    alpha=FAVOR_COVERAGE_WEIGHT,
) -> float:
    return alpha * similarity_score + (1 - alpha) * impact_score


def __cumulative_strength_of(links):
    return sum(link.strength for link in links)


def __vos_network_from(
    representative_items: List[Item],
    vos_network: VosNetwork,
) -> VosNetwork:
    links = __links_between(representative_items, vos_network.links)
    ordered_items = []
    for item in representative_items:
        if item not in ordered_items:
            ordered_items.append(item)
            neighbors = __neighbor_items_of(item, links, representative_items)
            ordered_items.extend(
                [neighbor for neighbor in neighbors if neighbor not in ordered_items]
            )

    return VosNetwork(
        items=ordered_items,
        links=links,
        clusters=vos_network.clusters,
    )


def __neighbor_items_of(item, links, items):
    neighbor_ids = set()
    for link in links:
        if link.source_id == item.id:
            neighbor_ids.add(link.target_id)
        elif link.target_id == item.id:
            neighbor_ids.add(link.source_id)

    return [item for item in items if item.id in neighbor_ids]


def __flattened_item_ids_from(cluster_id2representative_item_ids):
    return [
        item_id
        for item_ids in cluster_id2representative_item_ids.values()
        for item_id in item_ids
    ]


def __items_from_ids(item_ids: List[str], items: List[Item]) -> List[Item]:
    return [item for item in items if item.id in item_ids]


def __items_from(cluster_id: int, items: List[Item]) -> List[Item]:
    return [
        item
        for item in items
        if item.cluster == cluster_id and item.type != "ClusterLabel"
    ]


def __links_between(items: List[Item], total_links: List[Link]) -> List[Link]:
    item_ids = [item.id for item in items]
    return [
        link
        for link in total_links
        if link.source_id in item_ids and link.target_id in item_ids
        # and link.strength > 0.5
    ]


def __links_of(items: List[Item], total_links: List[Link]) -> List[Link]:
    item_ids = [item.id for item in items]
    return [
        link
        for link in total_links
        if link.source_id in item_ids or link.target_id in item_ids
    ]


def __link_exists(
    from_item_id: str,
    to_item_ids: List[str],
    links: List[Link],
) -> bool:
    return any(
        link.source_id == from_item_id
        and link.target_id in to_item_ids
        or link.target_id == from_item_id
        and link.source_id in to_item_ids
        for link in links
    )


def __log_stats(
    cluster_id2representative_item_ids: Dict[int, List[str]],
    vos_network: VosNetwork,
) -> None:
    cluster_ids = {item.cluster for item in vos_network.items}

    cluster_id2items_count = {
        cluster_id: len(__items_from(cluster_id, vos_network.items))
        for cluster_id in cluster_ids
    }
    cluster_id2representative_items_count = {
        cluster_id: len(representative_item_ids)
        for cluster_id, representative_item_ids in cluster_id2representative_item_ids.items()  # noqa E501
    }

    cluster_id2log = {
        cluster_id: f"{cluster_id2representative_items_count[cluster_id]} out of {cluster_id2items_count[cluster_id]}"  # noqa E501
        for cluster_id in cluster_id2items_count.keys()
    }

    logger.info(f"Representative items per cluster: {cluster_id2log}")
