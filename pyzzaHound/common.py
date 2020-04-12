import sys
import os
import logging
import logging.handlers
import socket

__registered_loggers__ = []

# create one instance of file handler, and only one
if not os.path.isdir('./log'):
    os.mkdir('./log')

_rtfh = logging.handlers.RotatingFileHandler(
    filename='log/pyzza.log',
    maxBytes=10000000,
    backupCount=10,
    mode='a'
)

_fmt = logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

_rtfh.setFormatter(_fmt)
_rtfh.setLevel(logging.INFO)

def get_logger(name):
    """
    Return a logger

    :param name:
    :return:
    """
    global __registered_loggers__
    if name not in __registered_loggers__:
        if not os.path.isdir('./log'):
            os.mkdir('./log')

        logger = logging.getLogger(name)
        logger.addHandler(_rtfh)

        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(_fmt)
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)
        __registered_loggers__.append(name)
    else:
        # return the registered logger
        logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger
