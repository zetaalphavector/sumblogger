from typing import cast

from src.bootstrap import RETRIEVE_DOCS_SERVICE, TEXT_COMPLETION_USECASE_CONFIG_REPO
from src.controllers.converters.vos_converters import (
    cluster2vos_from,
    to_vos_blogpost_response,
)
from src.controllers.v1.api_types import BlogpostConferenceItem, VosBlogpostItem
from src.handlers import commands
from src.handlers.text_completion import execute
from src.handlers.text_completion_usecases.blogpost_creator_from_cluster_summaries import (  # noqa E501
    build_usecase_command as blogpost_usecases_command,
)
from src.handlers.text_completion_usecases.summarize_documents_clusters import (
    build_usecases_command as summarize_usecases_command,
)
from src.handlers.vos_build_docs_clusters import to_documents_cluster
from src.handlers.vos_representative_docs import select_representative_docs
from src.types.vos import VosConferenceClusteredDocuments
from src.utils import inplace_clean_vos_network_of


async def generate_blogpost(
    body: VosConferenceClusteredDocuments,
    focus_on_most_representatives: bool = True,
    summary_words_limit: int = 100,
    detailed_paragraph_usecase_variant: str = "oneshot_detailed_paragraph",
    highlight_nodes_with_summaries: bool = True,
) -> BlogpostConferenceItem:
    try:
        inplace_clean_vos_network_of(body)

        if focus_on_most_representatives:
            representatives_cmd = commands.SelectVosRepresentativeDocuments(
                vos_network=body.network,
                top_k=int(summary_words_limit / 10),
            )
            vos_network = await select_representative_docs(representatives_cmd)
        else:
            vos_network = body.network

        id2documents_clusters = await to_documents_cluster(
            vos_network,
            RETRIEVE_DOCS_SERVICE,
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

        result = cast(
            VosBlogpostItem,
            await execute(usecase_cmd, TEXT_COMPLETION_USECASE_CONFIG_REPO),
        )

        vos = to_vos_blogpost_response(result["output_params"], body)

        return BlogpostConferenceItem(
            vos=vos, cluster2vos=cluster2vos_from(vos, highlight_nodes_with_summaries)
        )

    except Exception as e:
        print(f"Exception: {e}")
        raise e
