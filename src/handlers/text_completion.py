from typing import List, cast

from zav.message_bus import EventHandlerRegistry  # noqa F401
from zav.message_bus import CommandHandlerRegistry, Message

from src.controllers.v1.api_types import TextCompletionUsecaseItem
from src.handlers import commands
from src.services.text_completion.pass_through_service import (
    PassThroughTextCompletionService,
)
from src.services.text_completion.repository.usecase_config_repo import (
    TextCompletionUsecaseConfigRepository,
)
from src.services.text_completion.types import (
    PromptParams,
    TextCompletionServiceRequest,
)


@CommandHandlerRegistry.register(commands.ExecuteTextCompletionUsecase)
async def handle_text_completion_usecase(
    cmd: commands.ExecuteTextCompletionUsecase,
    queue: List[Message],
    pass_through_text_completion_service: PassThroughTextCompletionService,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecaseItem:

    usecase_config = await text_completion_usecase_config_repo.get_by(
        usecase=cmd.usecase,
        variant=cmd.variant,
    )

    prompt_params = cast(PromptParams, cmd.prompt_params)

    response = await pass_through_text_completion_service.execute(
        TextCompletionServiceRequest(
            usecase_config=usecase_config, params_list=[prompt_params]
        )
    )
    if response is None:
        raise ValueError("No response from text completion service.")

    return TextCompletionUsecaseItem(response=response["answers"][0])
