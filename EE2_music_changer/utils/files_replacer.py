import os
import shutil
from random import choice
from typing import List, Optional, Tuple

from .constants import GAME_MUSIC_NUMBER
from .paths_handler import get_platform_slash
from ..custom_logger import CustomLogger

REPLACER_LOGGER = CustomLogger("REPLACER_LOGGER")


def set_range(custom_files: List[str]) -> int:
    custom_music_number = len(custom_files)
    if custom_music_number >= GAME_MUSIC_NUMBER:
        return GAME_MUSIC_NUMBER
    return custom_music_number


def replace_file(input_path: str, output_path: str) -> None:
    shutil.copy(input_path, output_path)


def replace_music(
        game_files: List[str],
        custom_files: List[str],
        game_files_paths: List[str],
        custom_files_paths: List[str],
        rename_flag: Optional[bool] = None,
) -> Tuple[int, int]:
    loop_range = set_range(custom_files)
    renamed_counter = 0

    for index in range(loop_range):
        custom_music_path = custom_files_paths[index]
        REPLACER_LOGGER.show_info("Custom file #%d: %s", (index + 1), custom_music_path)

        if custom_files[index] in game_files:
            original_music_path_index = game_files.index(custom_files[index])
            original_music_path = game_files_paths[original_music_path_index]
            replace_file(custom_music_path, original_music_path)
        else:
            original_music_path = choice(game_files_paths)
            replace_file(custom_music_path, original_music_path)

            if rename_flag:
                renamed_counter += 1
                slash = get_platform_slash()
                custom_dir_path_list = custom_files_paths[0].split(slash)[:-1]
                original_music_filename = original_music_path.split(slash)[-1]
                custom_dir_path = os.path.join(slash, *custom_dir_path_list)
                new_filename_path = os.path.join(
                    custom_dir_path, original_music_filename
                )
                os.rename(custom_music_path, new_filename_path)
                REPLACER_LOGGER.show_info(
                    "Renamed file #%d: from '%s' to '%s'",
                    renamed_counter,
                    custom_music_path,
                    new_filename_path,
                )

        REPLACER_LOGGER.show_info(
            "Replaced file #%d: %s", (index + 1), original_music_path
        )

    return loop_range, renamed_counter
