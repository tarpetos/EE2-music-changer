import os
import shutil
from random import choice
from typing import List, Optional, Tuple

from .files_handler import get_music_files
from ..constants import GAME_MUSIC_NUMBER
from ..custom_logger import CustomLogger

REPLACER_LOGGER = CustomLogger("REPLACER_LOGGER")


def set_replace_music_value(custom_files: List[str]) -> int:
    custom_music_number = len(custom_files)
    return (
        GAME_MUSIC_NUMBER
        if custom_music_number >= GAME_MUSIC_NUMBER
        else custom_music_number
    )


def replace_file(input_path: str, output_path: str) -> None:
    shutil.copy(input_path, output_path)


def rename_music(custom_music_path: str, game_music_path: str) -> str:
    custom_dir_path = os.path.dirname(custom_music_path)
    game_music_filename = os.path.basename(game_music_path)
    renamed_custom_music_path = os.path.join(custom_dir_path, game_music_filename)
    os.rename(custom_music_path, renamed_custom_music_path)
    return renamed_custom_music_path


def replace_music(
    game_music_dir_path: str,
    game_files_paths: List[str],
    custom_files_paths: List[str],
    rename_flag: Optional[bool] = None,
) -> Tuple[int, int]:
    replace_music_value = set_replace_music_value(custom_files_paths)
    renamed_count = 0

    custom_files_paths_copy = custom_files_paths.copy()
    game_files_paths_copy = game_files_paths.copy()
    game_files = get_music_files(game_music_dir_path)

    for index in range(replace_music_value):
        custom_music_path = choice(custom_files_paths_copy)
        custom_files_paths_copy.remove(custom_music_path)
        custom_music_filename = os.path.basename(custom_music_path)

        REPLACER_LOGGER.show_info("Custom file #%d: %s", (index + 1), custom_music_path)
        if custom_music_filename in game_files:
            game_music_path_index = game_files.index(custom_music_filename)
            game_music_path = game_files_paths[game_music_path_index]
            replace_file(custom_music_path, game_music_path)
        else:
            game_music_path = choice(game_files_paths_copy)
            replace_file(custom_music_path, game_music_path)

            if rename_flag:
                renamed_custom_music_path = rename_music(
                    custom_music_path, game_music_path
                )
                renamed_count += 1
                REPLACER_LOGGER.show_info(
                    "Renamed file #%d: from '%s' to '%s'",
                    renamed_count,
                    custom_music_path,
                    renamed_custom_music_path,
                )

        game_files_paths_copy.remove(game_music_path)

        REPLACER_LOGGER.show_info("Replaced file #%d: %s", (index + 1), game_music_path)

    return replace_music_value, renamed_count
