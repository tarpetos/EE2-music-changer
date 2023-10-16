from EE2_music_changer import (
    find_ambient_dir_path,
    find_custom_dir_path,
    get_music_files,
    get_music_files_paths,
    replace_music,
    decompress,
)
from custom_logger import CustomLogger

MAIN_LOGGER = CustomLogger("MAIN_LOGGER")


def replace() -> None:
    music_path = find_ambient_dir_path()
    custom_music_path = find_custom_dir_path()

    try:
        music_files = get_music_files(music_path)
        music_files_paths = get_music_files_paths(music_path)
        custom_files = get_music_files(custom_music_path)
        custom_files_paths = get_music_files_paths(custom_music_path)
        MAIN_LOGGER.show_info("Music files: %s", music_files)
        MAIN_LOGGER.show_info("Music files paths: %s", music_files_paths)
        MAIN_LOGGER.show_info("Custom files: %s", custom_files)
        MAIN_LOGGER.show_info("Custom files paths: %s", custom_files_paths)
    except IndexError:
        MAIN_LOGGER.show_error("Path is empty or invalid!")
        return None
    replace_music(music_files, custom_files, music_files_paths, custom_files_paths)


def process_user_option() -> None:
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
            replace()
            break

        MAIN_LOGGER.show_warning("Invalid input! Must be '0' or '1'. Try again.")


def main() -> None:
    process_user_option()


if __name__ == "__main__":
    main()
