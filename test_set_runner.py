# pylint: disable=unused-wildcard-import,logging-not-lazy,bare-except,broad-except,eval-used,too-many-branches,singleton-comparison
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
import setup_functions
from parsing import group_tags
from tests.architecture import *


TEST_LIST = group_tags()

def _test_formatter(suite_list):
    count = 0
    success = 0
    fail = 0
    fail_list = []
    logger = setup_functions.setup_logger()
    suites_ran = []
	tests_ran = []
	
    for suite, tests in TEST_LIST.items():
        if suite in suite_list:
            suites_ran.append(suite)
            logger.info("#" * 75 + "\n" + " " * 12 + "#" * 75)
            logger.info("Starting new " + suite + " Test")
            for test in tests:
				tests_ran.append(test[1].replace("(logger)", ""))
				logger.info("*" * 75 + "\n" + " " * 12 + "*" * 75)
				logger.info("Running test: %s", test[1])
				error_list = []
				retries = 0
				while retries < 2:
					try:
						result = eval(test[0] + '.' + test[1])
						if result != False:
							success += 1
							break
						else:
							logger.error(test[1] + " has FAILED!!!")
							logger.info("The end state is not correct!!!")
							fail += 1
							fail_list.append(test[1].replace("(logger)", ""))
							break
					except Exception as error:
						retries += 1
						error_list.append(error)
						if retries >= 2:
							fail += 1
							fail_list.append(test[1].replace("(logger)", ""))
							logger.error("After 2 attempts, " + test[1] + " has FAILED!!!")
							logger.info("The list of errors encountered are\n" + " " * 12 + ("\n" + " " * 12).join(str(_test) for _test in error_list))

				count += 1

    logger.info(str(suites_ran) + " Testing has completed")
    logger.info("#" * 75)
    logger.info("Breakdown of tests:")
    logger.info("Tests ran: " + str(count) + "\n" + " " * 12 + ("\n" + " " * 12).join(str(_test) for _test in tests_ran))
    logger.info("Tests passed: " + str(success))
    logger.info("Tests failed: " + str(fail))
    if count == 0:
        logger.info("Pass rate: N/A")
    else:
        logger.info("Pass rate: " + str((success / count) * 100) + "%")
    if fail_list:
        logger.info("List of failed tests:\n" + " " * 12 + ("\n" + " " * 12).join(str(_test) for _test in fail_list))
    logger.info("#" * 75)



if __name__ == '__main__':
    # if all is specified then run all test suites
    if sys.argv[1] == "all":
       for suite in TEST_LIST.keys():
           _test_formatter(suite)

    # if multiple suits specified then run them
    elif len(sys.argv) > 2:
        TEST_SET = []
        for test in sys.argv:
            TEST_SET.append(test)
        TEST_SET.pop(0)

        for test in TEST_SET:
            _test_formatter(test)

    # if only one suit then run it
    else:
        if str(sys.argv[1]) in TEST_LIST.keys():
            _test_formatter([sys.argv[1]])
