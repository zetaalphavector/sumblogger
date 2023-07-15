import enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict


class ChatMessageSender(enum.Enum):
    USER = "user"
    BOT = "bot"


class ChatMessage(BaseModel):
    sender: ChatMessageSender
    content: str


class BotConversation(BaseModel):
    bot_setup_description: Optional[str]
    messages: List[ChatMessage] = []

    def user_sends(self, message: str):
        self.messages.append(
            ChatMessage(
                sender=ChatMessageSender.USER,
                content=message,
            )
        )

    def bot_sends(self, message: str):
        self.messages.append(
            ChatMessage(
                sender=ChatMessageSender.BOT,
                content=message,
            )
        )


class TextCompletionConfig(BaseModel):
    prompt_template: Optional[str]
    bot_conversation: Optional[BotConversation]


class LLMConfig(BaseModel):
    call_params: Dict[str, Any]
    text_completion_config: TextCompletionConfig


class TextCompletionUsecaseConfig(BaseModel):
    usecase: str
    variant: str
    version: int
    usecase_params: List[str]
    output_params: List[str]
    service_name: str
    llm_identifier_2_config: Dict[str, LLMConfig]


class PromptParams(Dict[str, Any]):
    ...


class SingleDocSummaryParams(PromptParams):
    document: str
    number_of_words: int


class TextCompletionServiceRequest(TypedDict):
    usecase_config: TextCompletionUsecaseConfig
    params: PromptParams


class TextCompletionServiceResponse(TypedDict):
    ...
