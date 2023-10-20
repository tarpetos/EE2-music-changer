import os
import sys

SAVE_PATH = os.path.join("EE2_music_changer", "default_music")


def get_reset_music_path() -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, SAVE_PATH)
    return os.path.join(SAVE_PATH)


RESET_MUSIC_FOLDER_NAME = get_reset_music_path()
MUSIC_FOLDER_NAME = "music"
MUSIC_CUSTOM_FOLDER_NAME = "custom_music"
DEFAULT_CUSTOM_DIR = "Documents"
AMBIENT_FOLDER_NAME = "Ambient"
EXE_FILE_NANE = "EE2.exe"
AVAILABLE_MUSIC_EXTENSION = "mp3"
OS_LINUX = "Linux"
OS_WINDOWS = "Windows"
GAME_MUSIC_NUMBER = 81
