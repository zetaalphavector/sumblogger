import asyncio
from typing import List

from zav.message_bus import EventHandlerRegistry  # noqa F401
from zav.message_bus import CommandHandlerRegistry, Message

from src.controllers.v1.api_types import TextCompletionParallelItem
from src.handlers import commands
from src.handlers.text_completion import handle_text_completion_usecase
from src.handlers.text_completion_chain import handle_text_completion_chain
from src.services.text_completion.pass_through_service import (
    PassThroughTextCompletionService,
)
from src.services.text_completion.repository.usecase_config_repo import (
    TextCompletionUsecaseConfigRepository,
)


@CommandHandlerRegistry.register(commands.ExecuteTextCompletionParallel)
async def handle_text_completion_parallel(
    cmd: commands.ExecuteTextCompletionParallel,
    queue: List[Message],
    pass_through_text_completion_service: PassThroughTextCompletionService,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionParallelItem:

    usecase_items = await asyncio.gather(
        *[
            __handle(
                usecase_cmd,
                queue,
                pass_through_text_completion_service,
                text_completion_usecase_config_repo,
            )
            for usecase_cmd in cmd.usecase_commands
        ]
    )

    return TextCompletionParallelItem(usecase_items=usecase_items)


async def __handle(
    usecase_cmd,
    queue,
    pass_through_text_completion_service,
    text_completion_usecase_config_repo,
):
    if isinstance(usecase_cmd, commands.ExecuteTextCompletionChain):
        return await handle_text_completion_chain(
            usecase_cmd,
            queue,
            pass_through_text_completion_service,
            text_completion_usecase_config_repo,
        )
    else:
        return await handle_text_completion_usecase(
            usecase_cmd,
            queue,
            pass_through_text_completion_service,
            text_completion_usecase_config_repo,
        )
