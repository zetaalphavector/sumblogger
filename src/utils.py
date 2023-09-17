def inplace_clean_vos_network_of(body):
    cluster_node_ids = [item.id for item in body.network.items if item.heading is None]
    body.network.items = [
        item for item in body.network.items if item.heading is not None
    ]
    body.network.links = [
        link
        for link in body.network.links
        if link.source_id not in cluster_node_ids
        and link.target_id not in cluster_node_ids
    ]
