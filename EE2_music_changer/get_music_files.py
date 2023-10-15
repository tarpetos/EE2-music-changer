import os
from typing import List

from .constants import AVAILABLE_MUSIC_EXTENSION


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


def get_music_files_paths(music_dir_path: str) -> List[str]:
    file_list = get_music_files(music_dir_path)
    file_paths_list = list(
        map(lambda filename: add_main_path(music_dir_path, filename), file_list)
    )
    return file_paths_list
