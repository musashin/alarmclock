import clock.clock as clock
import sys
import getopt
import unittest
import clockconfig
import utils.log as log
import multiprocessing
from threading import Timer

def execute_system_test(logger):
    """
    Execute the system test
    """
    logger.info('Executing System Test')

    suite = unittest.TestSuite()
    testmodules = [
        'utils.tests',
        'sound.tests'
    ]
    for t in testmodules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    if unittest.TextTestRunner(verbosity=2).run(suite):
        logger.info("System Test Passed Successfully")
    else:
        logger.error("System Test Failed")

    sys.exit()

def is_system_test():

    try:
        opts, args = getopt.getopt(sys.argv[1:],"t")
    except getopt.GetoptError:
        print 'clockmanager.py -t (optionnal)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            return True

    return False


def start_clock_process():
    p = multiprocessing.Process(target=clock.mainloop(), name='clock')
    p.start()

    return p

def monitor():

    print 'monitor'

    Timer(clockconfig.monitor_period_in_s, monitor).start()

if __name__ == '__main__':

    logger = log.create_logger()

    if is_system_test():
        execute_system_test(logger)
    else:
        clock_process = start_clock_process()

        Timer(clockconfig.monitor_period_in_s, monitor).start()
