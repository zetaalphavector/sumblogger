from enum import Enum


class SearchEngineString(str, Enum):
    ZETA_ALPHA = "zeta_alpha"
    GOOGLE_SCHOLAR = "google_scholar"

    def __str__(self) -> str:
        return str(self.value)
