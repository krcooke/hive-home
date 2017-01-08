#!/usr/bin/python

import logging
import logging.handlers

def setupLogger(log_path, verbose):
    logger = logging.getLogger('hive')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.handlers.TimedRotatingFileHandler(log_path, when="midnight", backupCount=5)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    if verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
