import clock.clock as clock
import sys
import getopt
import unittest
import logging
import logging.handlers
import os
import config

def execute_system_test():
    """
    Execute the system test
    """
    logger = logging.getLogger('clock')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
              os.path.join(config.log_folder,'clock.log.test'), maxBytes=4096, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
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
