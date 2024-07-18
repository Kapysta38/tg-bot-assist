import logging
from logging.handlers import RotatingFileHandler
import uuid


def get_logger(filename='logs/app.log', logger_name='app'):
    # Создание логгера
    logger = logging.getLogger(logger_name)

    # Проверка, если логгер уже настроен
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Формат логирования
        formatter = logging.Formatter('[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')

        # Обработчик для логирования в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Обработчик для логирования в файл с ротацией
        file_handler = RotatingFileHandler(filename, maxBytes=5 * 1024 * 1024, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
