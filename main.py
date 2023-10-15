from EE2_music_changer import (
    find_ambient_dir_path,
    find_custom_dir_path,
    get_music_files,
    get_music_files_paths,
    replace_music,
)


def main() -> None:
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


if __name__ == "__main__":
    main()
