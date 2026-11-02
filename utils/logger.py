"""统一日志：控制台 + 文件。"""
import logging
import sys

from utils.config_loader import PROJECT_ROOT, config

_LOGGER_NAME = "mall-autotest"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(_LOGGER_NAME)
    if logger.handlers:
        return logger

    level = str(config.get("log.level", "INFO")).upper()
    logger.setLevel(getattr(logging, level, logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    log_file = PROJECT_ROOT / str(config.get("log.file", "logs/autotest.log"))
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
