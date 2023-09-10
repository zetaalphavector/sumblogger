from fastapi import APIRouter, Depends
from zav.api.dependencies import get_message_bus
from zav.message_bus import MessageBus

from src.controllers.converters import to_vos_clustered_documents_response
from src.controllers.converters.vos_converters import (
    cluster2vos_from,
    to_vos_blogpost_response,
)
from src.controllers.v1.api_types import (
    BlogpostConferenceItem,
    DocumentsClustersSummariesItem,
    VosBlogpostItem,
)
from src.handlers import commands
from src.handlers.text_completion_usecases.blogpost_creator_from_cluster_summaries import (  # noqa E501
    build_usecase_command as blogpost_usecases_command,
)
from src.handlers.text_completion_usecases.summarize_documents_clusters import (
    build_usecases_command as summarize_usecases_command,
)
from src.types.conference_blog import ConferenceInfo
from src.types.vos import (
    VosClusteredDocuments,
    VosConferenceClusteredDocuments,
    VosNetwork,
)

vos_summaries_router = APIRouter(tags=["vos_summaries"])


@vos_summaries_router.post(
    "/vos/summaries",
    response_model=VosClusteredDocuments,
    status_code=200,
)
async def generate_vos_summaries(
    body: VosClusteredDocuments,
    focus_on_most_representatives: bool = True,
    summary_words_limit: int = 100,
    detailed_paragraph_usecase_variant: str = "oneshot_detailed_paragraph",
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        __inplace_clean_vos_network_of(body)

        if focus_on_most_representatives:
            vos_network = await __select_representatives(
                body, summary_words_limit, message_bus
            )
        else:
            vos_network = body.network

        id2documents_clusters = await __build_documents_clusters(
            message_bus, vos_network
        )

        usecase_cmd = summarize_usecases_command(
            id2documents_clusters,
            30,
            summary_words_limit,
            detailed_paragraph_usecase_variant,
        )
        results = await message_bus.handle(usecase_cmd)

        result: DocumentsClustersSummariesItem = results.pop(0)
        vos = to_vos_clustered_documents_response(result["output_params"], body)

        return vos
    except Exception as e:
        print(f"Exception: {e}")
        raise e


@vos_summaries_router.post(
    "/vos/blogpost",
    response_model=BlogpostConferenceItem,
    status_code=200,
)
async def generate_blogpost(
    body: VosConferenceClusteredDocuments,
    focus_on_most_representatives: bool = True,
    summary_words_limit: int = 100,
    detailed_paragraph_usecase_variant: str = "oneshot_detailed_paragraph",
    highlight_nodes_with_summaries: bool = True,
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        __inplace_clean_vos_network_of(body)

        if focus_on_most_representatives:
            vos_network = await __select_representatives(
                body, summary_words_limit, message_bus
            )
        else:
            vos_network = body.network

        id2documents_clusters = await __build_documents_clusters(
            message_bus, vos_network
        )

        summaries_usecase_cmd = summarize_usecases_command(
            id2documents_clusters,
            30,
            summary_words_limit,
            detailed_paragraph_usecase_variant,
        )
        usecase_cmd = blogpost_usecases_command(
            summaries_usecase_cmd,
            body.conference_info,
        )
        results = await message_bus.handle(usecase_cmd)

        result: VosBlogpostItem = results.pop(0)
        vos = to_vos_blogpost_response(result["output_params"], body)

        return BlogpostConferenceItem(
            vos=vos, cluster2vos=cluster2vos_from(body, highlight_nodes_with_summaries)
        )

    except Exception as e:
        print(f"Exception: {e}")
        raise e


async def __build_documents_clusters(message_bus, vos_network):
    return (
        await message_bus.handle(
            commands.BuildDocumentsClusters(vos_network=vos_network)
        )
    ).pop(0)


async def __select_representatives(
    body, summary_words_limit, message_bus
) -> VosNetwork:
    representative_vos: VosNetwork = (
        await message_bus.handle(
            commands.SelectVosRepresentativeDocuments(
                vos_network=body.network,
                top_k=int(summary_words_limit / 10),
            )
        )
    ).pop(0)
    return representative_vos


def __inplace_clean_vos_network_of(body):
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
