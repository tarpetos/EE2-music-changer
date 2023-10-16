from .custom_logger import CustomLogger
from .music_compressor import decompress
from .music_files_handler import get_music_files, get_music_files_paths
from .music_files_replacer import replace_music
from .music_path_handler import find_ambient_dir_path, find_custom_dir_path
from .types import FileType


class EE2MusicChanger:
    MAIN_LOGGER = CustomLogger("MAIN_LOGGER")
    GAME_FILE: FileType = "Game"
    CUSTOM_FILE: FileType = "Custom"

    def _replace(self) -> None:
        music_path = find_ambient_dir_path()
        custom_music_path = find_custom_dir_path()

        try:
            music_files = get_music_files(music_path)
            music_files_paths = get_music_files_paths(music_path, self.GAME_FILE)
            custom_files = get_music_files(custom_music_path)
            custom_files_paths = get_music_files_paths(
                custom_music_path, self.CUSTOM_FILE
            )
        except IndexError:
            self.MAIN_LOGGER.show_error("Path is empty or invalid!")
            return None
        replace_music(music_files, custom_files, music_files_paths, custom_files_paths)

    def process_user_option(self) -> None:
        while True:
            user_input = input(
                "Would you like to reset EE2 music to default or to change default music to custom music?\n"
                "0 - reset to default\n"
                "1 - change to custom\n"
                ">>>> "
            )
            if user_input == "0":
                decompress()
                break
            elif user_input == "1":
                self._replace()
                break

            self.MAIN_LOGGER.show_warning(
                "Invalid input! Must be '0' or '1'. Try again."
            )
