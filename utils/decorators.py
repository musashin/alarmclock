

def fail_if_exception(func):
    def inner(*args, **kwargs):
        ret = None

        if not hasattr(args[0], 'failed'):
            args[0].failed = False

        if args[0].failed:
            print 'not executing: failed'
        else:
            try:
                ret = func(*args, **kwargs)
            except Exception as e:
                args[0].failed = True
                print 'failed'

        return ret
    return inner


def return_false_if_exception(func):
    def inner(*args, **kwargs):
        if not hasattr(args[0], 'failed'):
            args[0].failed = False

        if args[0].failed:
            print 'not executing: failed'
        else:
            try:
                func(*args, **kwargs)
            except Exception as e:
                print 'return false'
                return False
            else:
                return True

    return inner

if __name__ =='__main__':

    class test:

        @fail_if_exception
        def testNoExcept(self):
            print 'OK'

        @return_false_if_exception
        def testNoExcept2(self):
            print 'OK2'

        @fail_if_exception
        def testWithExec(self):
            raise Exception

        @return_false_if_exception
        def testWithExec2(self):
            raise Exception

    mytest = test()

    mytest.testNoExcept2()
    mytest.testWithExec2()
    mytest.testNoExcept()
    mytest.testWithExec()
    mytest.testWithExec()
    print mytest