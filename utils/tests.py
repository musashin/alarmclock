import unittest
from decorators import *


class FatalDecoratorTests(unittest.TestCase):
    """
    Validate decorators that fail the object
    if an exception is raised running a method
    """
    def setUp(self):
        """
        Create a test object
        :return:
        """
        class test:

            @fail_if_exception
            def testNoExcept(self):
                self.HasExecuted = True

            @fail_if_exception
            def testWithExcept(self):
                self.HasExecuted = True
                raise Exception

        self.testObject = test()

    def tearDown(self):
        del self.testObject

    def testNoException(self):
        """
        Test Object has a failed member which is false
        when no exception is raised during execution
        """
        self.testObject.testNoExcept()
        self.assertFalse(self.testObject.failed)
        self.assertTrue(self.testObject.HasExecuted)

    def testException(self):
        """
        Test Object has a failed member which is True
        when no exception is raised during execution
        """
        self.testObject.testWithExcept()
        self.assertTrue(self.testObject.failed)
        self.assertTrue(self.testObject.HasExecuted)

        self.testObject.HasExecuted = False
        self.testObject.testNoExcept()
        self.assertFalse(self.testObject.HasExecuted)


class NonFatalDecoratorTests(unittest.TestCase):
    """
    Validate decorators that do not the object
    if an exception is raised running a method
    """
    def setUp(self):
        """
        Create a test object
        :return:
        """
        class test:

            @return_false_if_exception
            def testNoExcept(self):
                self.hasExecuted = True
                pass

            @return_false_if_exception
            def testWithExcept(self):
                self.hasExecuted = True
                raise Exception

        self.testObject = test()

    def tearDown(self):
        del self.testObject

    def testNoException(self):
        """
        Test Object has a failed member which is false
        when no exception is raised during execution
        """
        self.assertTrue(self.testObject.testNoExcept())
        self.assertFalse(self.testObject.failed)
        self.assertTrue(self.testObject.hasExecuted)

    def testException(self):
        """
        Test Object has a failed member which is True
        when no exception is raised during execution
        """
        self.assertFalse(self.testObject.testWithExcept())
        self.assertFalse(self.testObject.failed)
        self.assertTrue(self.testObject.hasExecuted)
