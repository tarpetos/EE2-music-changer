import platform

import flet as ft

from .app_ui import App, AppConfig
from .custom_logger import CustomLogger
from .constants import OS_LINUX, OS_WINDOWS


class EE2MusicChanger:
    MAIN_LOGGER = CustomLogger("MAIN_LOGGER")
    DEFAULT_APP_TITLE = "EE2 Music Changer"

    def __init__(self, app_title: str = DEFAULT_APP_TITLE):
        self.title = app_title

    def _init_ui(self, page: ft.Page) -> None:
        config = AppConfig(page, title=self.title)
        if platform.system() in (OS_LINUX, OS_WINDOWS):
            page.add(App((config.game_file_picker, config.custom_file_picker)))
        else:
            page.add(
                ft.Text(
                    "This application can only work on Linux distributions (Wine is required) and Windows OS."
                )
            )

    def start_app(self) -> None:
        self.MAIN_LOGGER.show_info("FLET APPLICATION STARTED")
        ft.app(target=self._init_ui)
        self.MAIN_LOGGER.show_info("FLET APPLICATION CLOSED")
