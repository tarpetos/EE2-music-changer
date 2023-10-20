from enum import Enum
from typing import Type, Literal


class FileType(Enum):
    GAME = "Game"
    CUSTOM = "Custom"

    def __str__(self) -> str:
        return self.value


FileTypeString: Type[str] = Literal["Game", "Custom"]


class CompressorOption(Enum):
    CUSTOM_COMPRESS = "custom_compress"
    SELENIUM_COMPRESS = "selenium_compress"
    DECOMPRESS = "decompress"
    RESET = "reset"


CompressorOptionString: Type[str] = Literal[
    "custom_compress", "selenium_compress", "decompress", "reset"
]
