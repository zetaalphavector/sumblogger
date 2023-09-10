from src.handlers.commands import (
    ExecuteTextCompletionSingleUsecase,
    ExecuteTextCompletionUsecases,
    UsecaseCommandsExecutionType,
)
from src.types.conference_blog import ConferenceInfo


def build_usecase_command(
    cluster_summaries_usecases: ExecuteTextCompletionUsecases,
    conference_info: ConferenceInfo,
):
    if cluster_summaries_usecases.params_mapping is None:
        raise ValueError("cluster_summaries_usecases.params_mapping must be set")

    cluster_summaries_usecases.params_mapping["intro_paragraph"] = "documents"

    return ExecuteTextCompletionUsecases(
        execution_type=UsecaseCommandsExecutionType.CHAIN,
        usecase_commands=[
            cluster_summaries_usecases,
            ExecuteTextCompletionUsecases(
                execution_type=UsecaseCommandsExecutionType.CHAIN,
                prompt_params=None,
                usecase_commands=[
                    ExecuteTextCompletionSingleUsecase(
                        usecase="titles_generation",
                        variant="title_per_intro_summary",
                        prompt_params={},
                        params_mapping={
                            "titles": "cluster_titles",
                            "documents": "topic_summaries",
                        },
                    ),
                    ExecuteTextCompletionSingleUsecase(
                        usecase="blog_surroundings",
                        variant="title_intro_conclusion",
                        prompt_params={"conference_info": conference_info},
                        params_mapping={
                            "title": "blog_title",
                            "intro": "blog_intro",
                            "conclusion": "blog_conclusion",
                            "topic_summaries": "intro_paragraphs",
                        },
                    ),
                ],
            ),
        ],
        params_mapping=None,
    )
