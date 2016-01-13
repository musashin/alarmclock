import alarmclock.clock as AlarmClock
import sys
import getopt
import unittest
import clockconfig
import utils.log as log
import multiprocessing
from multiprocessing import Queue
from threading import Timer
from gui import app


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


def start_clock_process(cmdsFromUI):

    p = multiprocessing.Process(target=AlarmClock.mainloop, name='alarmclock', args=(cmdsFromUI,))
    p.start()

    return p


def monitor():
    """
    Monitor System Health and Process State
    #TODO
    :return:
    """

    print 'monitor'

    start_monitor_thread()


def start_monitor_thread():
    """
    Monitor System Health and Process State
    #TODO
    :return:
    """
    Timer(clockconfig.monitor_period_in_s, monitor).start()


def start_user_interface_process():
    """
    Start the user interface process
    """
    p = multiprocessing.Process(target=app.run(debug=True, use_reloader=False, host='0.0.0.0'), name='gui')
    p.start()


def create_processes_shared_ressources():
    app.cmdsToClock = Queue()

    return (app.cmdsToClock,)

if __name__ == '__main__':

    logger = log.create_logger()

    if is_system_test():
        execute_system_test(logger)
    else:
        ui_to_clock_cmds, = create_processes_shared_ressources()

        start_clock_process(ui_to_clock_cmds)

        start_user_interface_process()

        start_monitor_thread()
