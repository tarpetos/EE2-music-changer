from typing import Type, Literal

FileType: Type[str] = Literal["Game", "Custom"]
CompressorOption: Type[str] = Literal["custom_compress", "selenium_compress", "decompress", "reset"]
