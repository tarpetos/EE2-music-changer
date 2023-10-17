import os
import time
from abc import ABC, abstractmethod
from typing import Optional, List
from pydub import AudioSegment
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from .custom_logger import CustomLogger
from .constants import (
    AVAILABLE_MUSIC_EXTENSION,
    GAME_MUSIC_NUMBER,
    SAVE_DIR,
)
from .files_handler import get_music_files, get_music_files_paths, search_default_music_files
from .files_replacer import replace_file
from .path_handler import find_ambient_dir_path, default_music_folder_check
from .types import CompressorOption

COMPRESSOR_LOGGER = CustomLogger("REPLACER_LOGGER")


class Compressor(ABC):
    @abstractmethod
    def compress(self, *args, **kwargs) -> None:
        raise NotImplementedError


class CustomCompressor(Compressor):
    FRAME_RATE = 44100
    CHANNEL_NUMER = 1
    SAMPLE_WIDTH = 4
    DEFAULT_BITRATE = "64k"
    COMPRESSION_BITRATE = "32k"

    def _base(self, input_file: str, output_file: str, bitrate: str) -> None:
        audio = AudioSegment.from_mp3(input_file)
        audio = (
            audio.set_frame_rate(self.FRAME_RATE)
            .set_channels(self.CHANNEL_NUMER)
            .set_sample_width(self.SAMPLE_WIDTH)
        )
        audio.export(output_file, format=AVAILABLE_MUSIC_EXTENSION, bitrate=bitrate)

    def compress(self, input_file: str, output_file: str) -> None:
        self._base(input_file, output_file, self.COMPRESSION_BITRATE)

    def decompress(self, input_file: str, output_file: str) -> None:
        self._base(input_file, output_file, self.DEFAULT_BITRATE)


class SeleniumCompressor(Compressor):
    URL = "https://www.onlineconverter.com/compress-mp3"
    SELENIUM_SAVE_DIR = os.path.abspath(SAVE_DIR)
    SELENIUM_LOAD_TIMEOUT = 60

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.SELENIUM_SAVE_DIR,
            },
        )
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(self.URL)

    def compress(self, input_file: str, filename: str) -> None:
        while True:
            try:
                self._get_file(input_file, filename)
                break
            except TimeoutException as e:
                COMPRESSOR_LOGGER.show_error("%s", e)
                continue

    def _get_file(self, input_file: str, filename: str) -> None:
        upload_file_input_xpath = "//input[@type='file']"
        file_input = self._select_element(upload_file_input_xpath)
        file_input.send_keys(input_file)

        convert_button_xpath = "//input[@type='button']"
        convert_button = self._select_element(convert_button_xpath)
        convert_button.click()

        download_xpath = "//div[@id='message']//a"
        download = self._select_element(download_xpath)
        download.click()

        self._file_downloading(self.driver, filename, self.SELENIUM_SAVE_DIR)

        self.driver.quit()

    def _select_element(self, xpath: str):
        return WebDriverWait(self.driver, self.SELENIUM_LOAD_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, xpath)
            )
        )

    def _file_downloading(
            self, driver: webdriver.Chrome, filename: str, dir_name: str
    ) -> None:
        start_time = time.perf_counter()
        downloaded_filename = filename.replace("_", "-")
        while time.perf_counter() - start_time < self.SELENIUM_LOAD_TIMEOUT:
            COMPRESSOR_LOGGER.show_info("Downloading %s...", filename)
            webdriver.ActionChains(driver).move_by_offset(0, 0).click().perform()
            if downloaded_filename in os.listdir(dir_name):
                os.rename(
                    src=os.path.join(dir_name, downloaded_filename),
                    dst=os.path.join(dir_name, filename),
                )
                break
            time.sleep(1)


class CompressorOptionSelector:
    CUSTOM_COMPRESS: CompressorOption = "custom_compress"
    SELENIUM_COMPRESS: CompressorOption = "selenium_compress"
    DECOMPRESS: CompressorOption = "decompress"
    RESET: CompressorOption = "reset"
    COMPRESSION_OPTIONS = (CUSTOM_COMPRESS, SELENIUM_COMPRESS)
    DECOMPRESSION_OPTIONS = (DECOMPRESS, RESET)

    def _base(
            self,
            option: CompressorOption,
            paths: List[str],
            music_files: List[str],
            saved_music_files: Optional[List[str]] = "",
            game_music_path: Optional[str] = ""
    ) -> None:
        for index, file_path in enumerate(paths):
            current_audio = music_files[index]
            save_path = os.path.join(SAVE_DIR, current_audio)
            progress = (100 * (index + 1)) / GAME_MUSIC_NUMBER
            if current_audio in saved_music_files and option in self.COMPRESSION_OPTIONS:
                COMPRESSOR_LOGGER.show_info(
                    "%.2f%% (%s already compressed). Skipped.", progress, current_audio
                )
                continue

            game_file_path = os.path.join(game_music_path, current_audio)

            if option == self.CUSTOM_COMPRESS:
                CustomCompressor().compress(file_path, save_path)
            elif option == self.SELENIUM_COMPRESS:
                SeleniumCompressor().compress(file_path, current_audio)
            elif option == self.DECOMPRESS:
                CustomCompressor().decompress(save_path, game_file_path)
            else:
                replace_file(save_path, game_file_path)

            if option in self.COMPRESSION_OPTIONS:
                COMPRESSOR_LOGGER.show_info(
                    "%.2f%% (%s compressed)", progress, current_audio
                )
            elif option in self.DECOMPRESSION_OPTIONS:
                COMPRESSOR_LOGGER.show_info(
                    "%.2f%% (%s placed into game folder)", progress, current_audio
                )

    def select(self, option: CompressorOption) -> None:
        if option == self.CUSTOM_COMPRESS or option == self.SELENIUM_COMPRESS:
            main_path = os.path.join(
                os.path.expanduser("~"),
                "Music",
                "music_ee2_default",
                "Ambient",  # insert path to default EE2 mp3 files
            )
            default_music_folder_check()
            paths = get_music_files_paths(main_path)
            music = get_music_files(main_path)
            saved_music = search_default_music_files()
            self._base(option, paths, music, saved_music_files=saved_music)
        else:
            paths = get_music_files_paths(SAVE_DIR)
            music = get_music_files(SAVE_DIR)
            music_path = find_ambient_dir_path()
            self._base(option, paths, music, game_music_path=music_path)
