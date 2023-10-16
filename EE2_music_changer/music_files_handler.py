import os
from typing import List, Optional

from .custom_logger import CustomLogger
from .constants import AVAILABLE_MUSIC_EXTENSION
from .types import FileType

FILE_LOGGER = CustomLogger("FILE_LOGGER")


def check_extensions(file_list: List[str]) -> List[str]:
    checked_file_list = [
        file for file in file_list if file.endswith(AVAILABLE_MUSIC_EXTENSION)
    ]
    return checked_file_list


def get_music_files(music_dir_path: str) -> List[str]:
    file_list = [files for root, dirs, files in os.walk(music_dir_path)][0]
    return check_extensions(file_list)


def add_main_path(main_path: str, filename: str) -> str:
    return os.path.join(main_path, filename)


def get_music_files_paths(music_dir_path: str, file: Optional[FileType] = None) -> List[str]:
    file_list = get_music_files(music_dir_path)
    file_paths_list = list(
        map(lambda filename: add_main_path(music_dir_path, filename), file_list)
    )
    if file:
        FILE_LOGGER.show_info("%s files: %s", file, file_list)
        FILE_LOGGER.show_info("%s files paths: %s", file, file_paths_list)
    return file_paths_list
