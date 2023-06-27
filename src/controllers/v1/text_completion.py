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
        responses = await message_bus.handle(
            ExecuteTextCompletionUsecase(
                usecase=body["usecase"],
                variant=body["variant"],
                prompt_params_list=body["prompt_params_list"],
                params_mapping=body["params_mapping"],
            )
        )
        response: TextCompletionUsecaseItem = responses.pop(0)
        return response
    except Exception as e:
        print(e)
        return {"error": str(e)}
