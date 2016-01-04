import clock.clock as clock
import sys
import getopt
import unittest
import clockconfig
import utils.log as log

def execute_system_test():
    """
    Execute the system test
    """
    logger = log.get_logger('test', clockconfig.syslog_facility)
    logger.info('Executing System Test')

    suite = unittest.TestSuite()
    testmodules = [
        'utils.tests',
        #'sound.tests'
    ]
    for t in testmodules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    if unittest.TextTestRunner(verbosity=2).run(suite):
        logger.info("System Test Passed Successfully")
    else:
        logger.error("System Test Failed")

    sys.exit()


if __name__ =='__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:],"t")
    except getopt.GetoptError:
        print 'startclock.py -t (optionnal)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            execute_system_test()

    clock.mainloop()
