from typing import List, Optional

from jinja2 import Template

from src.services.text_completion.types import (
    BotConversation,
    ChatMessage,
    PromptParams,
    TextCompletionConfig,
)


class TextCompletionConfigParser:
    @staticmethod
    def parse_template(
        template: Optional[str],
        params: PromptParams,
    ) -> Optional[str]:
        if template is None:
            return None

        return Template(template).render(**params)

    @staticmethod
    def __parse_bot_setup_description(description: Optional[str], params: PromptParams):
        if description is None:
            return None

        return TextCompletionConfigParser.parse_template(description, params)

    @staticmethod
    def __parse_chat_message(message: ChatMessage, params: PromptParams):
        return ChatMessage.parse_obj(
            {
                **message.dict(exclude={"content"}),
                "content": TextCompletionConfigParser.parse_template(
                    message.content, params
                ),
            },
        )

    @staticmethod
    def __parse_bot_conversation(
        bot_conversation: Optional[BotConversation], params: PromptParams
    ) -> Optional[BotConversation]:
        if bot_conversation is None:
            return None

        return BotConversation.parse_obj(
            {
                **bot_conversation.dict(exclude={"bot_setup_description", "messages"}),
                "bot_setup_description": TextCompletionConfigParser.__parse_bot_setup_description(  # noqa: E501
                    bot_conversation.bot_setup_description, params
                ),
                "messages": [
                    TextCompletionConfigParser.__parse_chat_message(message, params)
                    for message in bot_conversation.messages
                ],
            },
        )

    @staticmethod
    def parse(
        config: TextCompletionConfig, params: PromptParams
    ) -> TextCompletionConfig:
        return TextCompletionConfig.parse_obj(
            {
                **config.dict(exclude={"prompt_template", "bot_conversation"}),
                "prompt_template": TextCompletionConfigParser.parse_template(
                    config.prompt_template, params
                ),
                "bot_conversation": TextCompletionConfigParser.__parse_bot_conversation(
                    config.bot_conversation, params
                ),
            },
        )

    @staticmethod
    def parse_many(
        config: TextCompletionConfig,
        params_list: List[PromptParams],
    ) -> List[TextCompletionConfig]:
        return [
            TextCompletionConfigParser.parse(config, params) for params in params_list
        ]
