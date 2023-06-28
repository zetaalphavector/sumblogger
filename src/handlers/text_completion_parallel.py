import asyncio
from typing import List, cast

from zav.message_bus import EventHandlerRegistry  # noqa F401
from zav.message_bus import CommandHandlerRegistry, Message

from src.controllers.v1.api_types import (
    TextCompletionParallelItem,
    TextCompletionUsecaseItem,
)
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

    usecase_items: List[TextCompletionUsecaseItem] = await asyncio.gather(
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

    if cmd.should_flatten:
        usecase_items = __merge_output_params_lists(usecase_items)

    return TextCompletionParallelItem(usecase_items=usecase_items)


def __merge_output_params_lists(
    usecase_items: List[TextCompletionUsecaseItem],
) -> List[TextCompletionUsecaseItem]:
    merged = {
        "output_params_list": [{} for _ in usecase_items[0]["output_params_list"]]
    }
    for item in usecase_items:
        for i, output_param in enumerate(item["output_params_list"]):
            for key, value in output_param.items():
                if key not in merged["output_params_list"][i]:
                    merged["output_params_list"][i][key] = []
                if isinstance(value, list):
                    merged["output_params_list"][i][key].extend(value)
                else:
                    merged["output_params_list"][i][key].append(value)

    return [cast(TextCompletionUsecaseItem, merged)]


async def __handle(
    usecase_cmd,
    queue,
    pass_through_text_completion_service,
    text_completion_usecase_config_repo,
) -> TextCompletionUsecaseItem:
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
