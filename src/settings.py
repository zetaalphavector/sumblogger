import os

from src.services.text_completion.client import TextCompletionClientConfig

OPENAI_COMPLETION_TEMPERATURE = float(os.getenv("OPENAI_COMPLETION_TEMPERATURE", "0.0"))
OPENAI_COMPLETION_LOGPROBS = int(os.getenv("OPENAI_COMPLETION_LOGPROBS", "0"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_ORG = os.getenv("OPENAI_ORG", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "")
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE", "")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "")
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "")
OPENAI_DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_DEFAULT_TEMPERATURE", "0.0"))

DEFAULT_TEXT_COMPLETION_CLIENT_CONFIG = TextCompletionClientConfig(
    openai_api_key=OPENAI_API_KEY,
    openai_org=OPENAI_ORG,
    openai_api_base=OPENAI_API_BASE,
    openai_api_type=OPENAI_API_TYPE,
    openai_api_version=OPENAI_API_VERSION,
    model_name=OPENAI_DEFAULT_MODEL,
    openai_temperature=OPENAI_DEFAULT_TEMPERATURE,
)
