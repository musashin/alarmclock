import clock.clock as clock
import sound.sound as sound
import sys
import getopt


if __name__ =='__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:],"t")
    except getopt.GetoptError:
        print 'digitalclock.py -t (optionnal)'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            print 'Executing System Test'
            sound.test()
            sys.exit()

    clock.mainloop()
