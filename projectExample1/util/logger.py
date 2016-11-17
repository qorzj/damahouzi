import logging


def init_logger(path=''):
    logger = logging.getLogger(__name__)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(path) if path else logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s() - %(levelname)s => %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("init logger done")
    return logger