import os

import flet as ft
from typing import List

from ..constants import GAME_MUSIC_NUMBER, DEFAULT_CUSTOM_DIR, MUSIC_CUSTOM_FOLDER_NAME, MUSIC_FOLDER_NAME, \
    AMBIENT_FOLDER_NAME
from ..types import FileType, FileTypeString, CompressorOption, CompressorOptionString
from ..utils.paths_handler import get_platform_start_path, check_create_custom_dir, is_game_folder_selected
from ..utils.files_handler import get_music_files, get_music_files_paths
from ..utils.files_replacer import replace_music
from ..utils.audio_compressor import CompressorOptionSelector


def has_same_names(game_files: List[str], custom_files: List[str]) -> bool:
    return not all(custom_file in game_files for custom_file in custom_files)


class CallbackHandler(ft.UserControl):
    DARK_MODE: str = "Dark Mode"
    LIGHT_MODE: str = "Light Mode"
    TEXT_BUTTON_DARK_MODE_PADDING: int = 20
    TEXT_BUTTON_LIGHT_MODE_PADDING: int = 25
    GAME_FILE: FileTypeString = FileType.GAME
    CUSTOM_FILE: FileTypeString = FileType.CUSTOM
    RESET: CompressorOptionString = CompressorOption.RESET
    ERROR_DIALOG = "ERROR"
    SUCCESS_DIALOG = "SUCCESS"

    def __init__(self):
        super().__init__()
        self.change_button_option = None

    def change_button_callback(
            self,
            event: ft.ControlEvent,
            game_input_path: ft.TextField,
            custom_path_input: ft.TextField,
    ) -> None:
        check_create_custom_dir()

        try:
            self._change(game_input_path, custom_path_input)
        except IndexError:
            self._info_alert_dialog(
                self.ERROR_DIALOG, "Invalid or empty game music path! \nTry to set it manually."
            )

    def _change(
            self,
            game_input_path: ft.TextField,
            custom_path_input: ft.TextField,
    ) -> None:
        self.music_path = game_input_path.value
        self.custom_music_path = custom_path_input.value
        self.update()
        self.music_files = get_music_files(self.music_path)
        self.music_files_paths = get_music_files_paths(self.music_path, self.GAME_FILE)
        self.custom_files = get_music_files(self.custom_music_path)
        self.custom_files_paths = get_music_files_paths(self.custom_music_path, self.CUSTOM_FILE)
        if not self._music_paths_alerts():
            return

        has_same = has_same_names(self.music_files, self.custom_files)
        if has_same:
            self._rename_option_select()
        else:
            self.replace_counter = replace_music(self.music_path, self.music_files_paths, self.custom_files_paths)[0]

            self._info_alert_dialog(
                self.SUCCESS_DIALOG, f"{self.replace_counter} file(s) was/were successfully replaced."
            )

    def _music_paths_alerts(self) -> bool:
        if not self.music_files_paths and not self.custom_files_paths:
            message = "Game and custom music folders are empty!"
        elif not self.music_files_paths:
            message = "Game music folder is empty!"
        elif not self.custom_files_paths:
            message = "Custom music folder is empty!"
        else:
            return True

        self._info_alert_dialog(self.ERROR_DIALOG, message)
        return False

    def _rename_option_select(self) -> None:
        self.rename_dialog = ft.AlertDialog(
            title=ft.Text("Confirm renaming"),
            content=ft.Text("Do you want to rename custom files with game file names?"),
            actions=[
                ft.TextButton("Yes", on_click=self._change_button_yes_selected),
                ft.TextButton("No", on_click=self._change_button_no_selected),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.rename_dialog
        self.rename_dialog.open = True
        self.page.update()

    def _change_button_yes_selected(self, event: ft.ControlEvent) -> None:
        self.rename_dialog.open = False
        self.change_button_option = True
        self.page.update()
        self.replace_counter = replace_music(
            self.music_path,
            self.music_files_paths,
            self.custom_files_paths,
            self.change_button_option
        )
        self._info_alert_dialog(
            self.SUCCESS_DIALOG,
            f"{self.replace_counter[0]} file(s) was/were successfully "
            f"replaced and {self.replace_counter[1]} renamed."
        )

    def _change_button_no_selected(self, event: ft.ControlEvent) -> None:
        self.rename_dialog.open = False
        self.change_button_option = False
        self.page.update()
        self.replace_counter = replace_music(self.music_path, self.music_files_paths, self.custom_files_paths)
        self._info_alert_dialog(
            self.SUCCESS_DIALOG, f"{self.replace_counter[0]} file(s) was/were successfully replaced."
        )

    def reset_button_callback(
            self,
            event: ft.ControlEvent,
            game_input_path: ft.TextField,
    ) -> None:
        try:
            self._reset(game_input_path)
        except IndexError:
            self._info_alert_dialog(
                self.ERROR_DIALOG, "Invalid or empty music game path! \nTry to set it manually."
            )

    def _reset(
            self,
            game_input_path: ft.TextField,
    ) -> None:
        music_path = game_input_path.value
        if os.path.exists(music_path):
            option_selector = CompressorOptionSelector()
            option_selector.select(self.RESET, game_music_path=music_path)
            self._info_alert_dialog(
                self.SUCCESS_DIALOG, f"{GAME_MUSIC_NUMBER} files were successfully replaced."
            )
        else:
            self._info_alert_dialog(self.ERROR_DIALOG, "Invalid game path selected!")

    def game_path_button_callback(
            self,
            event: ft.ControlEvent,
            file_picker: ft.FilePicker,
    ) -> None:
        file_picker.get_directory_path(
            dialog_title="Set path to the game executable...",
            initial_directory=get_platform_start_path()[-1],
        )
        self.page.update()

    def custom_path_button_callback(
            self,
            event: ft.ControlEvent,
            file_picker: ft.FilePicker,
    ) -> None:
        file_picker.get_directory_path(
            initial_directory=os.path.join(os.path.expanduser("~"), DEFAULT_CUSTOM_DIR, MUSIC_CUSTOM_FOLDER_NAME)
        )
        self.page.update()

    def app_theme_checkbox_callback(
            self, event: ft.ControlEvent, checkbox: ft.Checkbox, buttons: List[ft.ElevatedButton]
    ) -> None:
        if checkbox.value:
            self._theme_change(
                checkbox, ft.ThemeMode.DARK, buttons, self.DARK_MODE, self.TEXT_BUTTON_DARK_MODE_PADDING)

        else:
            self._theme_change(
                checkbox, ft.ThemeMode.LIGHT, buttons, self.LIGHT_MODE, self.TEXT_BUTTON_LIGHT_MODE_PADDING
            )

        self.update()
        self.page.update()

    def file_picker_callback(
            self,
            event: ft.FilePickerResultEvent,
            input_path: ft.TextField,
    ) -> None:
        selected_path = event.path
        if selected_path is None:
            return

        if is_game_folder_selected(selected_path):
            input_path.value = os.path.join(selected_path, MUSIC_FOLDER_NAME, AMBIENT_FOLDER_NAME)
        else:
            self._info_alert_dialog(
                self.ERROR_DIALOG,
                "Game music path is invalid! Selected path does not contain necessary game structure."
            )
            input_path.value = "INVALID SELECTED PATH"
        self.update()

    def _theme_change(
            self,
            checkbox: ft.Checkbox,
            theme_mode: ft.ThemeMode,
            buttons: List[ft.ElevatedButton],
            mode_label: str,
            padding_value: int
    ) -> None:
        checkbox.label = mode_label
        self.page.theme_mode = theme_mode
        for button in buttons:
            button.style.padding = padding_value

    def _info_alert_dialog(self, title: str, message: str) -> ft.AlertDialog:
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Ok", on_click=lambda _: (setattr(dialog, "open", False), self.page.update())),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        return dialog
