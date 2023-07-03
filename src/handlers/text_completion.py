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
from src.settings import DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG
from src.types.text_completion import PromptParams, TextCompletionServiceRequest


async def __execute_single(
    cmd: commands.ExecuteTextCompletionSingleUsecase,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:

    usecase_config = await text_completion_usecase_config_repo.get_by(
        usecase=cmd.usecase,
        variant=cmd.variant,
    )

    prompt_params = cast(PromptParams, cmd.prompt_params)

    service = TextCompletionServiceFactory.create(
        usecase_config.service_name,
        DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG,
    )
    response_params = await service.execute(
        TextCompletionServiceRequest(
            usecase_config=usecase_config,
            params=prompt_params,
            should_flatten=cmd.should_flatten,
        )
    )
    if response_params is None:
        raise ValueError("No response from text completion service.")

    output_params = __map_output_params_list(cmd, response_params)

    return TextCompletionUsecasesItem(output_params=output_params)


def __map_output_params_list(
    cmd: Union[
        commands.ExecuteTextCompletionUsecases,
        commands.ExecuteTextCompletionSingleUsecase,
    ],
    response_params: Dict[str, Any],
) -> Dict[str, Any]:

    if cmd.params_mapping is None:
        return response_params

    output_params: Dict[str, Any] = {}
    for key, value in response_params.items():
        if key in cmd.params_mapping:
            output_params[cmd.params_mapping[key]] = value
        else:
            output_params[key] = value

    return output_params


async def execute_chain(
    cmd: commands.ExecuteTextCompletionUsecases,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:
    params = merge_two_param_dicts(cmd.prompt_params, {})

    for usecase_cmd in cmd.usecase_commands:
        usecase_cmd.prompt_params = merge_two_param_dicts(
            params, usecase_cmd.prompt_params
        )

        usecase_item = await __execute(
            usecase_cmd,
            text_completion_usecase_config_repo,
        )

        params = usecase_item["output_params"]

    return TextCompletionUsecasesItem(output_params=params)


async def execute_parallel(
    cmd: commands.ExecuteTextCompletionUsecases,
    text_completion_usecase_config_repo: TextCompletionUsecaseConfigRepository,
) -> TextCompletionUsecasesItem:
    for usecase_cmd in cmd.usecase_commands:

        usecase_cmd.prompt_params = merge_two_param_dicts(
            cmd.prompt_params,
            usecase_cmd.prompt_params,
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

    item = __merge_output_params(usecases_items)
    output_params = __map_output_params_list(cmd, item["output_params"])
    return TextCompletionUsecasesItem(output_params=output_params)


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


def __merge_output_params(
    usecase_items: List[TextCompletionUsecasesItem],
) -> TextCompletionUsecasesItem:
    output_params_dicts = [item["output_params"] for item in usecase_items]
    key2count = {}
    for output_params in output_params_dicts:
        for key in output_params.keys():
            if key not in key2count:
                key2count[key] = 0
            key2count[key] += 1

    merged = {}
    for output_params in output_params_dicts:
        for key, value in output_params.items():
            if key2count[key] == 1:
                merged[key] = value
            else:
                if key not in merged:
                    merged[key] = []
                merged[key].append(value)

    return TextCompletionUsecasesItem(output_params=merged)


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


def merge_two_param_dicts(
    params_1: Optional[Dict[str, Any]],
    params_2: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    if params_1 is None or params_2 is None:
        return params_1 or params_2 or {}
    else:
        return {
            **params_1,
            **params_2,
        }
