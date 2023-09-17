from typing import cast

from src.bootstrap import RETRIEVE_DOCS_SERVICE, TEXT_COMPLETION_USECASE_CONFIG_REPO
from src.controllers.converters.vos_converters import (
    to_vos_clustered_documents_response,
)
from src.controllers.v1.api_types import DocumentsClustersSummariesItem
from src.handlers import commands
from src.handlers.text_completion import execute
from src.handlers.text_completion_usecases.summarize_documents_clusters import (
    build_usecases_command as summarize_usecases_command,
)
from src.handlers.vos_build_docs_clusters import to_documents_cluster
from src.handlers.vos_representative_docs import select_representative_docs
from src.types.vos import VosClusteredDocuments
from src.utils import inplace_clean_vos_network_of


async def generate_vos_summaries(
    body: VosClusteredDocuments,
    focus_on_most_representatives: bool = True,
    summary_words_limit: int = 100,
    detailed_paragraph_usecase_variant: str = "oneshot_detailed_paragraph",
):
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

        usecase_cmd = summarize_usecases_command(
            id2documents_clusters,
            30,
            summary_words_limit,
            detailed_paragraph_usecase_variant,
        )
        result = cast(
            DocumentsClustersSummariesItem,
            await execute(usecase_cmd, TEXT_COMPLETION_USECASE_CONFIG_REPO),
        )
        vos = to_vos_clustered_documents_response(result["output_params"], body)

        return vos
    except Exception as e:
        print(f"Exception: {e}")
        raise e
