from loguru import logger
from loguru._logger import Logger


def get_logger(name: str, rotation="5 MB") -> Logger:
    a = logger.add(f'./logs/{name}.log', format="{time} {level} {name}:{function}:{line} {message}",
               level="ERROR", rotation=rotation, compression="zip")
    return logger
