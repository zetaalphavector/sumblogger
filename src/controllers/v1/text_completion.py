from typing import Union, cast

from fastapi import APIRouter, Depends
from zav.api.dependencies import get_message_bus
from zav.message_bus import MessageBus

from src.controllers.v1.api_types import (
    TextCompletionChainForm,
    TextCompletionChainItem,
    TextCompletionParallelForm,
    TextCompletionParallelItem,
    TextCompletionUsecaseForm,
    TextCompletionUsecaseItem,
)
from src.handlers.commands import (
    ExecuteTextCompletionChain,
    ExecuteTextCompletionParallel,
    ExecuteTextCompletionUsecase,
)

text_completion_router = APIRouter(tags=["text_completion"])


@text_completion_router.post(
    "/text_completion/pass_through",
    response_model=TextCompletionUsecaseItem,
    status_code=200,
)
async def pass_through_usecase(
    body: TextCompletionUsecaseForm,
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        responses = await message_bus.handle(__usecase_command_from(body))
        response: TextCompletionUsecaseItem = responses.pop(0)
        return response
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}


def __usecase_command_from(body: TextCompletionUsecaseForm):
    return ExecuteTextCompletionUsecase(
        usecase=body["usecase"],
        variant=body["variant"],
        prompt_params_list=body["prompt_params_list"],
        params_mapping=body["params_mapping"] if "params_mapping" in body else None,
        should_flatten=body["should_flatten"] if "should_flatten" in body else False,
    )


@text_completion_router.post(
    "/text_completion/chain",
    response_model=TextCompletionChainItem,
    status_code=200,
)
async def pass_through_chain(
    body: TextCompletionChainForm,
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        responses = await message_bus.handle(
            ExecuteTextCompletionChain(
                usecase_commands=[
                    __usecase_command_from(cmd) for cmd in body["chain_usecase_forms"]
                ]
            )
        )
        response: TextCompletionChainItem = responses.pop(0)
        return response
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}


def __command_from(
    form: Union[TextCompletionUsecaseForm, TextCompletionChainForm],
):
    if "chain_usecase_forms" in form:
        form = cast(TextCompletionChainForm, form)
        return ExecuteTextCompletionChain(
            usecase_commands=[
                __usecase_command_from(cmd) for cmd in form["chain_usecase_forms"]
            ]
        )
    else:
        form = cast(TextCompletionUsecaseForm, form)
        return __usecase_command_from(form)


@text_completion_router.post(
    "/text_completion/parallel",
    response_model=TextCompletionParallelItem,
    status_code=200,
)
async def pass_through_parallel(
    body: TextCompletionParallelForm,
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        responses = await message_bus.handle(
            ExecuteTextCompletionParallel(
                usecase_commands=[
                    __command_from(cmd) for cmd in body["parallel_usecase_forms"]
                ],
                should_flatten=body["should_flatten"],
            )
        )
        response: TextCompletionParallelItem = responses.pop(0)
        return response
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}
