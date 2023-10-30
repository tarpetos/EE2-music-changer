import os
import platform
import psutil
from typing import Optional, List

from ..constants import (
    OS_LINUX,
    OS_WINDOWS,
    MUSIC_FOLDER_NAME,
    MUSIC_CUSTOM_FOLDER_NAME,
    EXE_FILE_NAME,
    AMBIENT_FOLDER_NAME,
    DEFAULT_CUSTOM_DIR,
    RESET_MUSIC_FOLDER_NAME,
)
from ..custom_logger import CustomLogger

PATH_LOGGER = CustomLogger("PATH_LOGGER")


def get_platform_start_path() -> Optional[List[str]]:
    if platform.system() == OS_LINUX:
        linux_search_locations = [
            os.path.join(os.path.expanduser("~"), ".wine", "drive_c"),
            os.path.join(os.path.expanduser("~"), "Games"),
            os.path.join(os.path.expanduser("~")),
        ]
        return linux_search_locations
    elif platform.system() == OS_WINDOWS:
        windows_search_locations = [
            partition.device
            for partition in psutil.disk_partitions()
            if partition.device and partition.mountpoint
        ]
        return windows_search_locations


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
    main_dir_path = os.path.dirname(exe_path)
    music_path = os.path.join(main_dir_path, MUSIC_FOLDER_NAME)
    game_music_path = check_path_existence(music_path)

    return game_music_path


def find_ambient_dir_path() -> Optional[str]:
    start_dirs = get_platform_start_path()

    for start_dir in start_dirs:
        exe_path = find_path(start_dir, EXE_FILE_NAME)
        music_path = find_music_dir_path(exe_path)
        ambient_path = os.path.join(music_path, AMBIENT_FOLDER_NAME)
        if os.path.exists(ambient_path):
            PATH_LOGGER.show_info("Game music path: %s", ambient_path)
            return ambient_path


def check_create_custom_dir() -> str:
    start_dir = os.path.join(os.path.expanduser("~"), DEFAULT_CUSTOM_DIR)
    custom_dir_path = os.path.join(start_dir, MUSIC_CUSTOM_FOLDER_NAME)
    if not os.path.exists(custom_dir_path):
        os.mkdir(custom_dir_path)
        PATH_LOGGER.show_info("Custom music folder created at: %s", custom_dir_path)

    return custom_dir_path


def find_custom_dir_path() -> str:
    start_dir = check_create_custom_dir()
    # dir_path = find_path(start_dir, MUSIC_CUSTOM_FOLDER_NAME)
    custom_dir_path = check_path_existence(start_dir)
    PATH_LOGGER.show_info("Custom music path: %s", custom_dir_path)

    return custom_dir_path


def default_music_folder_check() -> None:
    if not os.path.exists(RESET_MUSIC_FOLDER_NAME):
        os.makedirs(RESET_MUSIC_FOLDER_NAME)
        PATH_LOGGER.show_info(
            "Music changer default audio folder created at: %s",
            os.path.abspath(RESET_MUSIC_FOLDER_NAME),
        )


def is_game_folder_selected(selected_path: str) -> bool:
    return all(item in os.listdir(selected_path) for item in [EXE_FILE_NAME, MUSIC_FOLDER_NAME])
