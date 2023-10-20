import os
import platform
from typing import Optional

from .constants import (
    OS_LINUX,
    OS_WINDOWS,
    MUSIC_FOLDER_NAME,
    MUSIC_CUSTOM_FOLDER_NAME,
    EXE_FILE_NANE,
    AMBIENT_FOLDER_NAME,
    DEFAULT_CUSTOM_DIR,
    RESET_MUSIC_FOLDER_NAME,
)
from ..custom_logger import CustomLogger

PATH_LOGGER = CustomLogger("PATH_LOGGER")


def get_platform_slash() -> str:
    return "\\" if platform.system() == OS_WINDOWS else "/"


def get_platform_start_path() -> Optional[str]:
    if platform.system() == OS_LINUX:
        return os.path.join(os.path.expanduser("~"), ".wine", "drive_c")
    elif platform.system() == OS_WINDOWS:
        return os.path.join(os.path.expanduser("~"))


def find_path(start_dir: str, dir_or_filename: str) -> str:
    for root, dirs, files in os.walk(start_dir):
        PATH_LOGGER.show_info("Search in: %s %s %s", root, dirs, files)
        if dir_or_filename in files or dir_or_filename in dirs:
            return os.path.abspath(os.path.join(root, dir_or_filename))
    return f"'{dir_or_filename}' not found in any directories."


def check_path_existence(path: str) -> str:
    if os.path.exists(path):
        return path
    return f"{path}"


def find_music_dir_path(exe_path: str) -> str:
    slash = get_platform_slash()
    main_dir_path = exe_path.split(slash)[:-1]
    music_path = os.path.join(slash, *main_dir_path, MUSIC_FOLDER_NAME)
    game_music_path = check_path_existence(music_path)

    return game_music_path


def find_ambient_dir_path() -> str:
    start_dir = get_platform_start_path()
    exe_path = find_path(start_dir, EXE_FILE_NANE)
    music_path = find_music_dir_path(exe_path)
    ambient_path = os.path.join(music_path, AMBIENT_FOLDER_NAME)
    ambient_music_path = check_path_existence(ambient_path)
    PATH_LOGGER.show_info("Game music path: %s", ambient_music_path)

    return ambient_music_path


def find_custom_dir_path() -> str:
    start_dir = os.path.join(os.path.expanduser("~"), DEFAULT_CUSTOM_DIR)
    custom_dir_path = os.path.join(start_dir, MUSIC_CUSTOM_FOLDER_NAME)
    if not os.path.exists(custom_dir_path):
        os.mkdir(custom_dir_path)
        PATH_LOGGER.show_info("Custom music folder created at: %s", custom_dir_path)
    dir_path = find_path(start_dir, MUSIC_CUSTOM_FOLDER_NAME)
    custom_dir_path = check_path_existence(dir_path)
    PATH_LOGGER.show_info("Custom music path: %s", custom_dir_path)

    return custom_dir_path


def default_music_folder_check() -> None:
    if not os.path.exists(RESET_MUSIC_FOLDER_NAME):
        os.makedirs(RESET_MUSIC_FOLDER_NAME)
        PATH_LOGGER.show_info(
            "Music changer default audio folder created at: %s",
            os.path.abspath(RESET_MUSIC_FOLDER_NAME),
        )
