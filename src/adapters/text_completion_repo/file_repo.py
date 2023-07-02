import json
import os
from collections import defaultdict
from typing import Dict, List

from pydantic import parse_obj_as

from src.services.text_completion.repository.usecase_config_repo import (
    TextCompletionUsecaseConfigRepository,
)
from src.types.text_completion import TextCompletionUsecaseConfig


class FileTextCompletionUsecaseConfigRepository(TextCompletionUsecaseConfigRepository):
    """
    This class is responsible for loading all prompt usecase configurations from a
    given directory.
    """

    def __init__(self, config_dir: str):
        self.__usecase2variant2config: Dict[
            str, Dict[str, TextCompletionUsecaseConfig]
        ] = self.__load_text_completion_usecase_config(config_dir)

    def __load_text_completion_usecase_config(
        self, prompt_configuration_dir: str
    ) -> Dict[str, Dict[str, TextCompletionUsecaseConfig]]:
        usecase2variant2config: Dict[
            str, Dict[str, TextCompletionUsecaseConfig]
        ] = defaultdict()

        for file in os.listdir(prompt_configuration_dir):
            if file.endswith(".json"):
                usecase_name = file.split(".json")[0]
                usecase2variant2config[usecase_name] = defaultdict()
                with open(os.path.join(prompt_configuration_dir, file)) as f:
                    usecase_configs = parse_obj_as(
                        List[TextCompletionUsecaseConfig],
                        json.load(f),
                    )
                    for usecase_config in usecase_configs:
                        usecase2variant2config[usecase_name][
                            usecase_config.variant
                        ] = usecase_config
        return usecase2variant2config

    async def get_by(self, usecase: str, variant: str) -> TextCompletionUsecaseConfig:
        if usecase not in self.__usecase2variant2config:
            raise ValueError(f"Usecase {usecase} not found.")

        if variant not in self.__usecase2variant2config[usecase]:
            raise ValueError(f"Variant {variant} not found for Usecase {usecase}.")

        return self.__usecase2variant2config[usecase][variant]
