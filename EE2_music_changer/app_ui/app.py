import flet as ft
from typing import Optional, Tuple
from .callbacks import CallbackHandler
from ..constants import AMBIENT_FOLDER_NAME, MUSIC_CUSTOM_FOLDER_NAME
from ..utils.paths_handler import find_ambient_dir_path, find_custom_dir_path


class App(CallbackHandler):
    # TODO: Fix reset button path selection +
    # TODO: Remove possibility to select random dirs +
    # TODO: Fix bug with repeated replacement of the same files +
    # TODO: Fix path selector height +
    # TODO: Fix cross-platform support +-
    # TODO: Add clever replacement with drag and drop music selection
    # TODO: Add possibility to somehow replace music for each epoch
    # TODO: Add MP3 compressor mode

    ROW_SPACING = 20
    COLUMN_SPACING = 30
    TEXT_BUTTON_BORDER_RADIUS = 5
    PATH_BUTTON_PADDING = 20

    def __init__(self, file_pickers: Tuple[ft.FilePicker, ft.FilePicker]):
        super().__init__()
        self.game_file_picker = file_pickers[0]
        self.game_file_picker.on_result = lambda pick_event: self.file_picker_callback(
            pick_event, self.game_path_input
        )
        self.custom_file_picker = file_pickers[1]
        self.custom_file_picker.on_result = (
            lambda pick_event: self.file_picker_callback(
                pick_event, self.custom_path_input
            )
        )

        self.change_button = ft.ElevatedButton(
            text="Change music",
            expand=True,
            on_click=lambda event: self.change_button_callback(
                event, self.game_path_input, self.custom_path_input
            ),
            tooltip="Changes the original music to a custom one (randomly or in accordance with the name of the files)."
        )

        self.clever_change_button = ft.ElevatedButton(
            text="Drag'n'drop music",
            expand=True,
            on_click=lambda event: self.clever_change_callback(
                event,
            ),
            tooltip="Changes the original music to a custom music, taken from different places."
        )

        self.reset_button = ft.ElevatedButton(
            text="Reset music",
            expand=True,
            on_click=lambda event: self.reset_button_callback(
                event, self.game_path_input
            ),
            tooltip="Overwrites 81 game music files with original music files.",
        )

        self.dark_mode_checkbox = ft.Checkbox(
            label=self.DARK_MODE,
            value=True,
            on_change=lambda event: self.app_theme_checkbox_callback(
                event,
                self.dark_mode_checkbox,
            ),
            tooltip="Changes application theme mode.",
        )

        self.game_path_input = ft.TextField(
            label="Game music folder path",
            value=find_ambient_dir_path(),
            autofocus=True,
            expand=True,
            read_only=True,
            tooltip=f"Absolute path to the game music folder called '{AMBIENT_FOLDER_NAME}'.",
        )

        self.game_path_button = ft.ElevatedButton(
            text="Select path...",
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda event: self.game_path_button_callback(
                event, self.game_file_picker
            ),
            style=ft.ButtonStyle(
                padding=self.PATH_BUTTON_PADDING,
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                        radius=self.TEXT_BUTTON_BORDER_RADIUS
                    ),
                },
            ),
            tooltip=f"Specify the absolute path to the EE2 root folder.",
        )

        self.custom_path_input = ft.TextField(
            label="Custom music folder path",
            value=find_custom_dir_path(),
            autofocus=True,
            expand=True,
            read_only=True,
            tooltip=f"Absolute path to the custom music folder called '{MUSIC_CUSTOM_FOLDER_NAME}'.",
        )

        self.custom_path_button = ft.ElevatedButton(
            text="Select path...",
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda event: self.custom_path_button_callback(
                event, self.custom_file_picker
            ),
            style=ft.ButtonStyle(
                padding=self.PATH_BUTTON_PADDING,
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                        radius=self.TEXT_BUTTON_BORDER_RADIUS
                    ),
                },
            ),
            tooltip=f"Specify the absolute path to the custom music folder called '{MUSIC_CUSTOM_FOLDER_NAME}'.",
        )

        self.rows = [
            self.row_builder(
                self.change_button, self.clever_change_button, self.reset_button
            ),
            self.row_builder(self.dark_mode_checkbox),
            self.row_builder(self.game_path_input, self.game_path_button, spacing=None),
            self.row_builder(self.custom_path_input, spacing=None),
        ]

    def row_builder(
        self, *controls: ft.Control, spacing: Optional[int] = ROW_SPACING
    ) -> ft.Row:
        return ft.Row(
            controls=[*controls],
            spacing=spacing if spacing else 0,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def column_builder(self, *controls: ft.Control) -> ft.Column:
        return ft.Column(
            controls=[*controls],
            spacing=self.COLUMN_SPACING,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def build(self) -> ft.Column:
        return self.column_builder(*self.rows)
