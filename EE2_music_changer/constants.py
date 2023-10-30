import os
import sys


def get_reset_music_path() -> str:
    save_path = os.path.join("EE2_music_changer", "default_music")

    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, save_path)
    return os.path.join(save_path)


RESET_MUSIC_FOLDER_NAME = get_reset_music_path()
AMBIENT_FOLDER_NAME = "Ambient"
MUSIC_FOLDER_NAME = "music"
DEFAULT_CUSTOM_DIR = "Documents"
MUSIC_CUSTOM_FOLDER_NAME = "custom_music"
EXE_FILE_NAME = "EE2.exe"
AVAILABLE_MUSIC_EXTENSION = "mp3"
OS_LINUX = "Linux"
OS_WINDOWS = "Windows"
GAME_MUSIC_NUMBER = 81
