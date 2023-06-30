import asyncio
from typing import Any, Dict, List, Optional, Union, cast

from zav.message_bus import EventHandlerRegistry  # noqa F401
from zav.message_bus import CommandHandlerRegistry, Message

from src.controllers.v1.api_types import TextCompletionUsecasesItem
from src.handlers import commands
from src.services.text_completion.repository.usecase_config_repo import (
    TextCompletionUsecaseConfigRepository,
)
from src.services.text_completion.service_factory import TextCompletionServiceFactory
from src.services.text_completion.types import (
    PromptParams,
    TextCompletionServiceRequest,
)
from src.settings import DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG


async def __execute_single(
    cmd: commands.ExecuteTextCompletionSingleUsecase,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:

    usecase_config = await text_completion_usecase_config_repo.get_by(
        usecase=cmd.usecase,
        variant=cmd.variant,
    )

    prompt_params_list = [
        cast(PromptParams, prompt_params) for prompt_params in cmd.prompt_params_list
    ]

    service = TextCompletionServiceFactory.create(
        usecase_config.service_name,
        DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG,
    )
    response_params_list = await service.execute(
        TextCompletionServiceRequest(
            usecase_config=usecase_config,
            params_list=prompt_params_list,
            should_flatten=cmd.should_flatten,
        )
    )
    if response_params_list is None:
        raise ValueError("No response from text completion service.")

    output_params_list = []
    for response_params in response_params_list:
        if cmd.params_mapping is not None:
            for key, new_key in cmd.params_mapping.items():
                if key in response_params:
                    response_params[new_key] = response_params.pop(key)

        output_params_list.append(response_params)

    return TextCompletionUsecasesItem(output_params_list=output_params_list)


async def execute_chain(
    cmd: commands.ExecuteTextCompletionUsecases,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:
    params_list = merge_two_params_lists([], cmd.prompt_params_list)

    for usecase_cmd in cmd.usecase_commands:
        usecase_cmd.prompt_params_list = merge_two_params_lists(
            params_list, usecase_cmd.prompt_params_list
        )

        usecase_item = await __execute(
            usecase_cmd,
            text_completion_usecase_config_repo,
        )

        params_list = usecase_item["output_params_list"]

    return TextCompletionUsecasesItem(output_params_list=params_list)


async def execute_parallel(
    cmd: commands.ExecuteTextCompletionUsecases,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:
    for usecase_cmd in cmd.usecase_commands:
        usecase_cmd.prompt_params_list = merge_two_params_lists(
            cmd.prompt_params_list, usecase_cmd.prompt_params_list
        )

    usecases_items: List[TextCompletionUsecasesItem] = await asyncio.gather(
        *[
            __execute(
                usecase_cmd,
                text_completion_usecase_config_repo,
            )
            for usecase_cmd in cmd.usecase_commands
        ]
    )

    return __merge_output_params_lists(usecases_items)


EXECUTION_TYPE_TO_HANDLER = {
    commands.UsecaseCommandsExecutionType.CHAIN: execute_chain,
    commands.UsecaseCommandsExecutionType.PARALLEL: execute_parallel,
}


async def __execute(
    cmd: Union[
        commands.ExecuteTextCompletionSingleUsecase,
        commands.ExecuteTextCompletionUsecases,
    ],
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:
    if isinstance(cmd, commands.ExecuteTextCompletionSingleUsecase):
        return await __execute_single(
            cmd,
            text_completion_usecase_config_repo,
        )
    elif isinstance(cmd, commands.ExecuteTextCompletionUsecases):
        handler = EXECUTION_TYPE_TO_HANDLER[cmd.execution_type]
        return await handler(
            cmd,
            text_completion_usecase_config_repo,
        )


@CommandHandlerRegistry.register(commands.ExecuteTextCompletionUsecases)
async def handle_text_completion_usecases(
    cmd: commands.ExecuteTextCompletionUsecases,
    queue: List[Message],
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:
    return await __execute(
        cmd,
        text_completion_usecase_config_repo,
    )


def __merge_output_params_lists(
    usecase_items: List[TextCompletionUsecasesItem],
) -> TextCompletionUsecasesItem:
    merged = {
        "output_params_list": [{} for _ in usecase_items[0]["output_params_list"]]
    }
    for item in usecase_items:
        for i, output_param in enumerate(item["output_params_list"]):
            for key, value in output_param.items():
                if key not in merged["output_params_list"][i]:
                    merged["output_params_list"][i][key] = []
                merged["output_params_list"][i][key].append(value)

    return cast(TextCompletionUsecasesItem, merged)


def merge_two_params_lists(
    params_list_1: Optional[List[Dict[str, Any]]],
    params_list_2: Optional[List[Dict[str, Any]]],
):
    if params_list_1 is None:
        return []
    if params_list_2 is None:
        return []

    all_usecase_params = []
    for index in range(max(len(params_list_1), len(params_list_2))):
        params = params_list_1[index] if index < len(params_list_1) else {}
        usecase_params = params_list_2[index] if index < len(params_list_2) else {}
        all_usecase_params.append({**params, **usecase_params})
    return all_usecase_params
