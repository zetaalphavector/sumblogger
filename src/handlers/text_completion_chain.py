from typing import List

from zav.message_bus import EventHandlerRegistry  # noqa F401
from zav.message_bus import CommandHandlerRegistry, Message

from src.controllers.v1.api_types import TextCompletionChainItem
from src.handlers import commands
from src.handlers.text_completion import handle_text_completion_usecase
from src.services.text_completion.pass_through_service import (
    PassThroughTextCompletionService,
)
from src.services.text_completion.repository.usecase_config_repo import (
    TextCompletionUsecaseConfigRepository,
)


@CommandHandlerRegistry.register(commands.ExecuteTextCompletionChain)
async def handle_text_completion_chain(
    cmd: commands.ExecuteTextCompletionChain,
    queue: List[Message],
    pass_through_text_completion_service: PassThroughTextCompletionService,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionChainItem:

    params_list = []

    for usecase_cmd in cmd.usecase_commands:
        all_usecase_params = []
        for index in range(max(len(params_list), len(usecase_cmd.prompt_params_list))):
            params = params_list[index] if index < len(params_list) else {}
            usecase_params = (
                usecase_cmd.prompt_params_list[index]
                if index < len(usecase_cmd.prompt_params_list)
                else {}
            )
            all_usecase_params.append({**params, **usecase_params})

        usecase_cmd.prompt_params_list = all_usecase_params

        usecase_item = await handle_text_completion_usecase(
            usecase_cmd,
            queue,
            pass_through_text_completion_service,
            text_completion_usecase_config_repo,
        )

        params_list = usecase_item["output_params_list"]

    return TextCompletionChainItem(output_params_list=params_list)
