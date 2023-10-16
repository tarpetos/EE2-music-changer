import logging

from abc import ABC, abstractmethod


class BaseLogger(ABC):
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def show_info(self, info_data: str) -> None:
        return self.logger.info(info_data)

    def show_warning(self, warn_data: str) -> None:
        return self.logger.warning(warn_data)
