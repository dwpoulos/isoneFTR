import logging
import os


def get_logger():
    logger = logging.getLogger("neiso")
    logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d '
                                  '- %(message)s')

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('ftr_logger.log', 'a')
    file_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)
    return logger


logger = get_logger()