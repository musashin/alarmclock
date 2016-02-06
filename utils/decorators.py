"""
This module provides a set of decorators for class methods
This decorator provide a generalize way to deal with exceptions around the following
principle:
 - The object is added a failed attribute.
 - If the failed attribute is true, decorated methods are skipped
 - Depending on the decorator used, any exception raised will either set the failed
 attribute or affected the function returned value

 All exceptions are logged with a ERROR severity on the 'clock' logger.
"""

import logging
import clockconfig
from mpd import ConnectionError

def fail_if_exception(func):
    """
    This decorator will:
    - Not execute the decorated method if the method object as a failed attribute True
    - Set failed attribute true if the method execution raised an exception.

    :param func: decorated function
    :return: True if no exception is raised, false otherwise
    """
    def inner(*args, **kwargs):
        ret = None

        if not hasattr(args[0], 'failed'):
            args[0].failed = False

        if not args[0].failed:
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                args[0].failed = True
                logging.getLogger(clockconfig.app_name).exception("{!s} failed".format(func.__name__))
        return ret
    return inner


def return_false_if_exception(func):
    """
    This decorator will:
    - Not execute the decorated method if the method object as a failed attribute True
    - Otherwise, catch all exceptions, 'pokemon style' and return true
    if the method did not raise an exception, false otherwise

    :param func: decorated function
    :return: True if no exception is raised, false otherwise
    """
    def inner(*args, **kwargs):
        if not hasattr(args[0], 'failed'):
            args[0].failed = False

        if not args[0].failed:
            try:
                func(*args, **kwargs)
            except ConnectionError as e:
                if 'connect' in dir(args[0]):
                    args[0].connect()
                    func(*args, **kwargs)
            except Exception as e:
                logging.getLogger(clockconfig.app_name).exception("{!s} failed".format(func.__name__))
                return False
            else:
                return True

    return inner

