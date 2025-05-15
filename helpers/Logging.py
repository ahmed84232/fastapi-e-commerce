import logging


def get_logger(name):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt="%(levelname)s: %(asctime)s [%(module)s]: %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename="app.log")

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.handlers = [stream_handler, file_handler]
    logger.setLevel(logging.DEBUG)

    return logger