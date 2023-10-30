import flet as ft


class AppConfig:
    WIDTH = 850
    HEIGHT = 450
    PADDING = 20

    def __init__(self, page: ft.Page, title: str):
        self.page = page
        self.page.title = title
        self.page.window_width = self.WIDTH
        self.page.window_height = self.HEIGHT
        self.page.window_min_width = self.WIDTH
        self.page.window_min_height = self.HEIGHT
        self.page.padding = self.PADDING
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.dark_theme = ft.Theme(color_scheme_seed=ft.colors.INDIGO_ACCENT)
        self.game_file_picker = ft.FilePicker()
        self.custom_file_picker = ft.FilePicker()
        self.page.overlay.append(self.game_file_picker)
        self.page.overlay.append(self.custom_file_picker)
        self.page.update()
