#pylint: disable=unused-wildcard-import,logging-not-lazy,bare-except,broad-except,eval-used,too-many-branches,singleton-comparison
'''
Created on Feb 28, 2019

@author: erik.kniaz

Exec discoveries:
By running any of the below functions, if we initialize a logger object within the function and have exec
call another function, the logger object is treated as a local variable of the function called by exec.
Because of this we do not need to pass any arguments to the exec function to run with the code it executes.
We can verify this by printing the local vars in any function below and comparing it to the local vars of
the function being called by exec.

'''
import sys
import common_functions
from decorators import group_tags
from tests.architecture import * #import all tests under the architecture folder
from tests.infrastructure import * #import all tests under the infrastructure folder


SMOKE_TESTS, UNIT_TESTS, FUNCTIONAL_TESTS, REGRESSION_TESTS = group_tags()

def _test_formatter(suite):
    if suite == "smoke":
        test_list = SMOKE_TESTS
    if suite == "unit":
        test_list = UNIT_TESTS
    if suite == "functional":
        test_list = FUNCTIONAL_TESTS
    if suite == "regression":
        test_list = REGRESSION_TESTS

    count = 0
    success = 0
    fail = 0
    fail_list = []
    logger = common_functions.setup_logger()
    logger.info("#"*75 + "\n" + " "*12 + "#"*75)
    logger.info("Starting new " + suite +" Test")
    for tst in test_list:
        logger.info("*"*75 + "\n" + " "*12 + "*"*75)
        logger.info("Running test: %s", tst[1])
        error_list = []
        retries = 0
        while retries < 2:
            try:
                result = eval(tst[0]+'.'+tst[1])
                if result != False:
                    success += 1
                    break
                else:
                    logger.error(tst[1] + " has FAILED!!!")
                    logger.info("The end state is not correct!!!")
                    fail += 1
                    fail_list.append(tst[1].replace("(logger)", ""))
                    break
            except Exception as error:
                retries += 1
                error_list.append(error)
                if retries >= 2:
                    fail += 1
                    fail_list.append(tst[1].replace("(logger)", ""))
                    logger.error("After 2 attempts, "+ tst[1] + " has FAILED!!!")
                    logger.info("The list of errors encountered are\n" + " "*12 + ("\n" + " "*12).join(str(_test) for _test in error_list))


        count += 1

    logger.info(suite + " Testing has completed")
    logger.info("#"*75)
    logger.info("Breakdown of tests:")
    logger.info("Tests ran: " + str(count))
    logger.info("Tests passed: " + str(success))
    logger.info("Tests failed: " + str(fail))
    if count == 0:
        logger.info("Pass rate: N/A")
    else:
        logger.info("Pass rate: " + str((success/count)*100) + "%")
    logger.info("List of failed tests:\n" + " "*12 + ("\n" + " "*12).join(str(_test) for _test in fail_list))
    logger.info("#"*75)

    if fail >= 1:
        if suite != 'all':
            sys.exit(-1)



def smoke_test():
    '''
    Runs all tests that have been tagged @smoke
    '''
    _test_formatter("smoke")

def unit_test():
    '''
    Runs all tests that have been tagged @unit
    '''
    _test_formatter("unit")

def functional_test():
    '''
    Runs all tests that have been tagged @functional
    '''
    _test_formatter("functional")

def regression_test():
    '''
    Runs all tests that have been tagged @regression
    '''
    _test_formatter("regression")


if __name__ == '__main__':
    #if all is specified then run all test suites
    if sys.argv[1] == "all":
        smoke_test()
        unit_test()
        functional_test()
        regression_test()

    #if multiple suits specified then run them
    elif len(sys.argv) > 2:
        TEST_SET = []
        for test in sys.argv:
            TEST_SET.append(test)
        TEST_SET.pop(0)

        for test in TEST_SET:
            exec(str(test)+"()")

    #if only one suit then run it
    else:
        exec(str(sys.argv[1])+"()")
        