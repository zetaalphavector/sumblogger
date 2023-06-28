from fastapi import APIRouter, Depends
from zav.api.dependencies import get_message_bus
from zav.message_bus import MessageBus

from src.controllers.v1.api_types import (
    TextCompletionUsecaseForm,
    TextCompletionUsecaseItem,
)
from src.handlers.commands import ExecuteTextCompletionUsecase

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
        responses = await message_bus.handle(usecase_command_from(body))
        response: TextCompletionUsecaseItem = responses.pop(0)
        return response
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": str(e)}


def usecase_command_from(body: TextCompletionUsecaseForm):
    return ExecuteTextCompletionUsecase(
        usecase=body["usecase"],
        variant=body["variant"],
        prompt_params_list=body["prompt_params_list"],
        params_mapping=body["params_mapping"] if "params_mapping" in body else None,
        should_flatten=body["should_flatten"] if "should_flatten" in body else False,
    )
