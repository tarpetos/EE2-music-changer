import os
import shutil
import time
from typing import List
from pydub import AudioSegment
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from .custom_logger import CustomLogger
from .constants import (
    FRAME_RATE,
    CHANNEL_NUMER,
    SAMPLE_WIDTH,
    AVAILABLE_MUSIC_EXTENSION,
    COMPRESSION_BITRATE,
    RESET_MUSIC_FOLDER_NAME,
    MAIN_FOLDER_NAME,
    DEFAULT_BITRATE,
    GAME_MUSIC_NUMBER,
    SELENIUM_LOAD_TIMEOUT,
)
from .music_files_handler import get_music_files, get_music_files_paths
from .music_path_handler import find_ambient_dir_path
from .types import CompressionType

COMPRESSOR_LOGGER = CustomLogger("REPLACER_LOGGER")
SAVE_DIR = os.path.join(MAIN_FOLDER_NAME, RESET_MUSIC_FOLDER_NAME)


def default_music_folder_check() -> None:
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def custom_compress(
    input_file: str, output_file: str, bitrate: str = DEFAULT_BITRATE
) -> None:
    audio = AudioSegment.from_mp3(input_file)
    audio = (
        audio.set_frame_rate(FRAME_RATE)
        .set_channels(CHANNEL_NUMER)
        .set_sample_width(SAMPLE_WIDTH)
    )
    audio.export(output_file, format=AVAILABLE_MUSIC_EXTENSION, bitrate=bitrate)


def selenium_compress(input_file: str, filename: str) -> None:
    dir_name = os.path.abspath(SAVE_DIR)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": dir_name,
        },
    )
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.onlineconverter.com/compress-mp3")

    upload_file_button_xpath = "//input[@type='file']"

    file_input = WebDriverWait(driver, SELENIUM_LOAD_TIMEOUT).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, upload_file_button_xpath)
        )
    )
    file_input.send_keys(input_file)

    convert_button_xpath = "//input[@type='button']"
    convert_button = WebDriverWait(driver, SELENIUM_LOAD_TIMEOUT).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, convert_button_xpath)
        )
    )
    convert_button.click()

    download_xpath = "//div[@id='message']//a"
    download = WebDriverWait(driver, SELENIUM_LOAD_TIMEOUT).until(
        expected_conditions.presence_of_element_located((By.XPATH, download_xpath))
    )
    download.click()

    selenium_file_downloading(driver, filename, dir_name)

    driver.quit()


def selenium_file_downloading(
    driver: webdriver.Chrome, filename: str, dir_name: str
) -> None:
    start_time = time.perf_counter()
    downloaded_filename = filename.replace("_", "-")
    while time.perf_counter() - start_time < SELENIUM_LOAD_TIMEOUT:
        COMPRESSOR_LOGGER.show_info("Downloading %s...", filename)
        webdriver.ActionChains(driver).move_by_offset(0, 0).click().perform()
        if downloaded_filename in os.listdir(dir_name):
            os.rename(
                src=os.path.join(dir_name, downloaded_filename),
                dst=os.path.join(dir_name, filename),
            )
            break
        time.sleep(1)


def selenium_compress_loop(file_path: str, current_audio: str) -> None:
    while True:
        try:
            selenium_compress(input_file=file_path, filename=current_audio)
            break
        except TimeoutException as e:
            COMPRESSOR_LOGGER.show_error("%s", e)
            continue


def search_default_music_files() -> List[str]:
    saved_music = [
        file
        for file in os.listdir(SAVE_DIR)
        if file.endswith(AVAILABLE_MUSIC_EXTENSION)
    ]
    return saved_music


def compress(compression_option: CompressionType) -> None:
    main_path = os.path.join(
        os.path.expanduser("~"),
        "Music",
        "music_ee2_default",
        "Ambient",  # insert path to default EE2 mp3 files
    )
    default_music_folder_check()
    music = get_music_files(main_path)
    paths = get_music_files_paths(main_path)
    saved_music = search_default_music_files()

    for index, file_path in enumerate(paths):
        current_audio = music[index]
        save_path = os.path.join(SAVE_DIR, current_audio)
        progress = round((100 * (index + 1)) / GAME_MUSIC_NUMBER, 2)
        if current_audio in saved_music:
            COMPRESSOR_LOGGER.show_info(
                "%.2f%% (%s already compressed). Skipped.)", progress, current_audio
            )
            continue

        if compression_option == "custom":
            custom_compress(
                input_file=file_path, output_file=save_path, bitrate=COMPRESSION_BITRATE
            )
        else:
            selenium_compress_loop(file_path, current_audio)
            COMPRESSOR_LOGGER.show_info(
                "%.2f%% (%s compressed)", progress, current_audio
            )


def decompress(change_bit_rate: bool = False) -> None:
    music_path = find_ambient_dir_path()
    music = get_music_files(SAVE_DIR)
    paths = get_music_files_paths(SAVE_DIR)

    for index, file_path in enumerate(paths):
        current_audio = music[index]
        saved_file = os.path.join(SAVE_DIR, current_audio)
        game_file_path = os.path.join(music_path, current_audio)
        progress = (100 * (index + 1)) / GAME_MUSIC_NUMBER
        if change_bit_rate:
            custom_compress(input_file=saved_file, output_file=game_file_path)
        else:
            shutil.copy(saved_file, game_file_path)

        COMPRESSOR_LOGGER.show_info(
            "%.2f%% (%s placed into game folder)", progress, current_audio
        )
