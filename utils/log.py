import logging
"""
Utility module to provide logging to the clock system components.

All logs are directed to 2 handlers:
    - All severities are directed to syslog daemon
    - Errors are also directed to prowl

"""
import clockconfig
import logging.handlers
import prowler
import clockconfig
import ConfigParser
import sys

def create_logger():
    """
    Create the clock logger
    """
    logger = logging.getLogger(clockconfig.app_name,)
    logger.setLevel(logging.DEBUG)

    syslog = logging.handlers.SysLogHandler(address='/dev/log', facility=clockconfig.syslog_facility)
    syslog.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(syslog)

    if clockconfig.development_environ:
        console = logging.StreamHandler(sys.stdout)
        logger.addHandler(console)

    __attach_prowl_handler(logger)

    return logger


def __attach_prowl_handler(logger):
    """
    Attach the prowl log handler for warning and errors
    :param logger: logger object
    :return:
    """
    try:
        configfile = ConfigParser.RawConfigParser()
        configfile.read(clockconfig.user_config_file)
        prowl = prowler.LogHandler(key=configfile.get('prowl', 'key'),
                                   app=clockconfig.app_name,
                                   event='error')
    except Exception as e:
        logger.error("Prowl service not available [{!s}]".format(e))

    prowl.setLevel(logging.WARNING)
    logger.addHandler(prowl)