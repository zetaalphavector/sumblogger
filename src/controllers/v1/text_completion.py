from typing import Union, cast

from fastapi import APIRouter, Depends
from zav.api.dependencies import get_message_bus
from zav.message_bus import MessageBus

from src.controllers.v1.api_types import (
    TextCompletionSingleUsecaseForm,
    TextCompletionUsecasesForm,
    TextCompletionUsecasesFormBase,
    TextCompletionUsecasesItem,
    UsecasesExecutionType,
)
from src.handlers.commands import (
    ExecuteTextCompletionSingleUsecase,
    ExecuteTextCompletionUsecases,
    UsecaseCommandsExecutionType,
)

text_completion_router = APIRouter(tags=["text_completion"])


@text_completion_router.post(
    "/text_completion/pass_through",
    response_model=TextCompletionUsecasesItem,
    status_code=200,
)
async def pass_through_usecase(
    body: TextCompletionUsecasesFormBase,
    message_bus: MessageBus = Depends(get_message_bus),
):
    try:
        body = cast(TextCompletionUsecasesForm, body)
        responses = await message_bus.handle(
            ExecuteTextCompletionUsecases(
                usecase_commands=[
                    __usecase_command_from(form) for form in body["usecase_forms"]
                ],
                execution_type=UsecaseCommandsExecutionType(
                    body["execution_type"].value
                ),
                prompt_params_list=body["prompt_params_list"],
            )
        )
        response: TextCompletionUsecasesItem = responses.pop(0)
        return response
    except Exception as e:
        raise e
        print(f"Exception: {e}")
        return {"error": str(e)}


def __usecase_command_from(
    form: Union[TextCompletionSingleUsecaseForm, TextCompletionUsecasesForm]
):
    if "usecase_forms" in form:
        usecases_form = cast(TextCompletionUsecasesForm, form)
        return ExecuteTextCompletionUsecases(
            usecase_commands=[
                __usecase_command_from(form) for form in usecases_form["usecase_forms"]
            ],
            execution_type=UsecaseCommandsExecutionType(
                usecases_form["execution_type"].value
                if isinstance(usecases_form["execution_type"], UsecasesExecutionType)
                else usecases_form["execution_type"]
            ),
            prompt_params_list=usecases_form["prompt_params_list"],
        )
    else:
        single_form = cast(TextCompletionSingleUsecaseForm, form)
        return ExecuteTextCompletionSingleUsecase(
            usecase=single_form["usecase"],
            variant=single_form["variant"],
            prompt_params_list=single_form["prompt_params_list"],
            should_flatten=single_form["should_flatten"]
            if "should_flatten" in single_form
            else False,
            params_mapping=single_form["params_mapping"]
            if "params_mapping" in single_form
            else None,
        )
