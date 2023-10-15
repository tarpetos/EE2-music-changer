import os
import platform
import tkinter as tk
from tkinter import filedialog
from typing import Optional

from .constants import (
    OS_LINUX,
    OS_WINDOWS,
    MUSIC_FOLDER_NAME,
    MUSIC_CUSTOM_FOLDER_NAME,
    EXE_FILE_NANE,
    AMBIENT_FOLDER_NAME,
    DEFAULT_CUSTOM_DIR,
)


def get_platform_slash() -> str:
    return "\\" if platform.system() == OS_WINDOWS else "/"


def custom_path() -> str:
    root = tk.Tk()
    root.withdraw()

    user_path = filedialog.askdirectory(title="Select a directory")
    if user_path:
        user_path = os.path.join(get_platform_slash(), user_path)
        return user_path
    return ""


def get_platform_start_path() -> Optional[str]:
    if platform.system() == OS_WINDOWS:
        return os.path.join(os.path.expanduser("~"), ".wine", "drive_c")
    elif platform.system() == OS_LINUX:
        return custom_path()


def find_path(start_dir: str, dir_or_filename: str) -> str:
    for root, dirs, files in os.walk(start_dir):
        print("Search in:", root, dirs, files)
        if dir_or_filename in files or dir_or_filename in dirs:
            return os.path.abspath(os.path.join(root, dir_or_filename))
    return f"'{dir_or_filename}' not found in any directories."


def check_path_existence(path: str) -> str:
    if os.path.exists(path):
        return path
    return f"'{path}' path does not exists."


def find_music_dir_path(exe_path: str) -> str:
    slash = get_platform_slash()
    main_dir_path = exe_path.split(slash)[:-1]
    music_path = os.path.join(slash, *main_dir_path, MUSIC_FOLDER_NAME)

    return check_path_existence(music_path)


def find_ambient_dir_path() -> str:
    start_dir = get_platform_start_path()
    exe_path = find_path(start_dir, EXE_FILE_NANE)
    music_path = find_music_dir_path(exe_path)
    ambient_path = os.path.join(music_path, AMBIENT_FOLDER_NAME)

    return check_path_existence(ambient_path)


def find_custom_dir_path() -> str:
    start_dir = os.path.join(os.path.expanduser("~"), DEFAULT_CUSTOM_DIR)
    dir_path = find_path(start_dir, MUSIC_CUSTOM_FOLDER_NAME)
    if not os.path.exists(dir_path):
        os.mkdir(os.path.join(start_dir, MUSIC_CUSTOM_FOLDER_NAME))

    return check_path_existence(dir_path)