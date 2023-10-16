import os
import shutil
from random import choice
from typing import List

from .constants import GAME_MUSIC_NUMBER
from .music_path_handler import get_platform_slash


def has_same_names(game_files: List[str], custom_files: List[str]) -> bool:
    return all(custom_file in game_files for custom_file in custom_files)


def rename_option_selected(has_same: bool) -> bool:
    while not has_same:
        rename_files = input("\nRename custom music with game music name [Y/N]?\n>>>> ")

        if rename_files.upper() == "Y":
            return True
        elif rename_files.upper() == "N":
            return False

        print("Invalid input! Try again.")


def set_range(custom_files: List[str]) -> int:
    custom_music_number = len(custom_files)
    if custom_music_number >= GAME_MUSIC_NUMBER:
        return GAME_MUSIC_NUMBER
    return custom_music_number


def replace_music(
    game_files: List[str],
    custom_files: List[str],
    game_files_paths: List[str],
    custom_files_paths: List[str],
) -> None:
    has_same = has_same_names(game_files, custom_files)
    rename_flag = rename_option_selected(has_same)
    loop_range = set_range(custom_files)

    for index in range(loop_range):
        custom_music_path = custom_files_paths[index]
        print(f"Custom file #{index + 1}:", custom_music_path)

        if custom_files[index] in game_files:
            original_music_path_index = game_files.index(custom_files[index])
            original_music_path = game_files_paths[original_music_path_index]
            shutil.copy(custom_music_path, original_music_path)
        else:
            original_music_path = choice(game_files_paths)
            shutil.copy(custom_music_path, original_music_path)

            if rename_flag:
                slash = get_platform_slash()
                custom_dir_path_list = custom_files_paths[0].split(slash)[:-1]
                original_music_filename = original_music_path.split(slash)[-1]
                custom_dir_path = os.path.join(slash, *custom_dir_path_list)
                new_filename_path = os.path.join(custom_dir_path, original_music_filename)
                print(new_filename_path)
                os.rename(custom_music_path, new_filename_path)

        print(f"Replaced file #{index + 1}:", original_music_path, "\n")
