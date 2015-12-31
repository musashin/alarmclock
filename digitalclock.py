import clock.clock as clock
import sound.sound as sound
import utils.tests
import sys
import getopt
import unittest


if __name__ =='__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:],"t")
    except getopt.GetoptError:
        print 'digitalclock.py -t (optionnal)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            print 'Executing System Test'
            suite = unittest.TestSuite()
            testmodules = [
                            'utils.tests',
                            'sound.tests'
                            ]
            for t in testmodules:
                suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
            unittest.TextTestRunner(verbosity=2).run(suite)
            sys.exit()

    clock.mainloop()
