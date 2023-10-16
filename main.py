from EE2_music_changer import (
    find_ambient_dir_path,
    find_custom_dir_path,
    get_music_files,
    get_music_files_paths,
    replace_music,
    decompress
)


def replace() -> None:
    music_path = find_ambient_dir_path()
    custom_music_path = find_custom_dir_path()

    try:
        print("\nMusic files:", music_files := get_music_files(music_path))
        print(
            "Music files paths:", music_files_paths := get_music_files_paths(music_path)
        )
        print("Custom files:", custom_files := get_music_files(custom_music_path))
        print(
            "Custom files paths:",
            custom_files_paths := get_music_files_paths(custom_music_path),
            "\n",
        )
    except IndexError:
        print("Path is empty or invalid!")
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

        print("Invalid input! Must be '0' or '1'. Try again.\n")


def main() -> None:
    process_user_option()


if __name__ == "__main__":
    main()
