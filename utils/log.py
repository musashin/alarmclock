import logging
import logging.handlers
import prowler
import clockconfig
import ConfigParser


def get_logger(subprocessname, facility):
    logger = logging.getLogger(clockconfig.app_name,)
    logger.setLevel(logging.DEBUG)

    syslog = logging.handlers.SysLogHandler(address='/dev/log', facility=facility)
    syslog.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(syslog)

    configfile = ConfigParser.RawConfigParser()
    configfile.read(clockconfig.user_config_file)
    prowl = prowler.LogHandler(key=configfile.get('prowl', 'key'),
                               app=clockconfig.app_name,
                               event='error')

    prowl.setLevel(logging.WARNING)
    logger.addHandler(prowl)

    return logger