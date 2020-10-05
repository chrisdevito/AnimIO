from __future__ import absolute_import

__title__ = 'CameraBatch'
__author__ = 'Christopher DeVito'
__email__ = 'chrisdevito@chribis.com'
__version__ = '0.1.0'
__license__ = 'MIT'
__description__ = ("A simple I/O tool that captures animation of an object"
                   " to an external file that can be reimported.")

import logging


def get_logger(debug=False):
    """
    Gets logger object

    :param debug: Sets logging to level DEBUG.
    :type debug: (bool)

    :return: logger
    :rtype: logger object
    """
    log = logging.getLogger("AnimIO")

    if not len(log.handlers):
        log_format = '%(asctime)-15s %(name)s [%(levelname)s] %(message)s'
        time_format = '%Y-%m-%d %H:%M:%S'
        log_formatter = logging.Formatter(
            log_format, time_format)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        log.addHandler(stream_handler)

        if debug:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)

        log.propagate = False

    return log


# get logging object
LOG = get_logger(debug=False)

# import show to make execution easier
from AnimIO.utils import show
