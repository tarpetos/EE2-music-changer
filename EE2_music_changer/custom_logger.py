import logging


class CustomLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s %(name)s %(levelname)s: | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def show_info(self, *args, **kwargs) -> None:
        self.logger.info(*args, **kwargs)

    def show_warning(self, message, *args, **kwargs) -> None:
        self.logger.warning(message, *args, **kwargs)

    def show_error(self, *args, **kwargs) -> None:
        self.logger.error(*args, **kwargs)
