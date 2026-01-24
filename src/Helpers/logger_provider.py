import logging
import pathlib
from logging.handlers import RotatingFileHandler


def get_logger() -> logging.Logger:
    logger = logging.getLogger("ImageConverter")
    logger.setLevel(logging.WARNING)

    logging_path = pathlib.Path(__file__).parents[2].joinpath("app_logs", "image_converter.log")
    logging_path.parent.mkdir(exist_ok=True, parents=True)

    if not logger.hasHandlers():
        handler = RotatingFileHandler(logging_path, maxBytes=5*1024*1024, backupCount=5)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s - %(funcName)s - %(lineno)d",
                                  datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger