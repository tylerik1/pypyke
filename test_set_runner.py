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
import platform
import setup_functions
import traceback

from parsing import group_tags, get_functions
from time import sleep
import time
from filelock import Timeout, FileLock
import pandas


from tests.architecture import *





logger = setup_functions.setup_logger()
#transfer_tests.transfer_js_debt_bem(logger, 'uat')
#piv_tests.login_prod(logger)

TEST_LIST = group_tags(logger)







def _test_formatter(suite_list, **kwargs):
    count = 0
    success = 0
    fail = 0
    fail_list = []
    logger = setup_functions.setup_logger()
    suites_ran = []
    tests_ran = []

    coverage_start = False

    for suite, tests in TEST_LIST.items():
        if suite == suite_list:
            suites_ran.append(suite)
            logger.info("#" * 75 + "\n" + " " * 12 + "#" * 75)
            logger.info("Starting new " + suite + " Test")
            for test in tests:
                tests_ran.append(test[1].replace("(logger, env=" + kwargs['env'] + ")", ""))
                logger.info("*" * 75 + "\n" + " " * 12 + "*" * 75)
                logger.info("Running test: %s", test[1].split("env='")[0] + "'" + kwargs['env'] + "')")
                error_list = []
                retries = 0

                while retries < 2:
                    common_functions.cleanup_chromedriver(logger)
                    sleep(1)

                    try:
                        driver = setup_functions.setup_driver(logger, str(test[1].split('(')[0]), performance_mode=False)
                    except Exception as e:
                        logger.info('Unable to create chromedriver instance.')
                        logger.info(e)
                        logger.info(traceback.print_exc())
                        continue






                    try:
                        #print(test[0])
                        #print(test[1])
                        #logger.info(test[0].split('.')[1] + '.' + test[1].split("env='")[0] + "'" + kwargs['env'] + "')")
                        if platform.system() == "Linux":
                            if suite == 'bulk_parallel_process':
                                if __name__ == '__main__':
                                    function = 'bulk_parallel_process: function = ' + str(kwargs['function'])
                                    result = parallel_processing.bulk_parallel_process(driver, logger, excel_file=kwargs['excel_file'],
                                                                                       sheet=kwargs['sheet'],
                                                                                       partitions=kwargs['partitions'], function=kwargs['function'], env=kwargs['env'])
                            else:
                                #formated as filename.testname(args)
                                function = test[1].replace("env='uat'", "env='"+kwargs['env'] + "'")
                                for key in kwargs:
                                    if key + '=' in function:
                                        function = function.replace(key + '=None', key + '=' + "'" + str(kwargs[key]) + "'")
                                result = eval(test[0][1:].split("/")[1] + '.' + function)
                        else:
                            if suite == 'bulk_parallel_process':
                                #print(test[0])
                                #print('9'*99)
                                #print(test[0] + '.bulk_parallel_process(logger, excel_file='+kwargs['excel_file']+', sheet='+kwargs['sheet'].strip("'")+ ', partitions='+kwargs['partitions']+ ', function='+kwargs['function']+ ', env='+kwargs['env']+ ')')
                                if __name__ == '__main__':
                                    function = 'bulk_parallel_process: function = ' + str(kwargs['function'])
                                    result = parallel_processing.bulk_parallel_process(driver, logger, excel_file=kwargs['excel_file'],
                                                                              sheet=kwargs['sheet'],
                                                                              partitions=kwargs['partitions'], function=kwargs['function'], env=kwargs['env'])
                            else:
                                function = test[1].replace("env='uat'", "env='"+kwargs['env'] + "'")

                                for key in kwargs:
                                    if key+'=' in function:
                                        function = function.replace(key + '=None', key + '=' + "'" + str(kwargs[key]) + "'")

                                result = eval(test[0].split('.')[1] + '.' + function)


                        if result:
                            driver.quit()
                            sleep(3)
                            success += 1
                            break
                        else:
                            try:
                                setup_functions.make_screenshot(driver, str(test[1].split('(')[0]), logger)
                            except Exception as e:
                                logger.info('Unable to create screenshot due to: ' + str(e))
                            driver.quit()
                            sleep(3)
                            logger.error(function + " has FAILED!!!")
                            fail += 1
                            fail_list.append(function)
                            break
                    except Exception as error:
                        logger.info(error)
                        logger.info(traceback.print_exc())
                        if 'Max retries exceeded' in str(error):
                            continue
                        if 'Connection refused' in str(error):
                            continue
                        if 'invalid session id' in str(error):
                            continue
                        retries += 1
                        error_list.append(error)
                        if str(test[1].split('(')[0]) != 'bulk_parallel_process':
                            try:
                                setup_functions.make_screenshot(driver, str(test[1].split('(')[0]), logger)
                            except Exception as e:
                                logger.info('Unable to create screenshot due to: ' + str(e))
                        if str(test[1].split('(')[0]) != 'bulk_parallel_process':
                            driver.quit()
                            sleep(3)
                        if retries >= 2:
                            fail += 1
                            fail_list.append(function)
                            logger.error("After 2 attempts, " + function + " has FAILED!!!")
                            logger.info("The list of errors encountered are\n" + " " * 12 + ("\n" + " " * 12).join(str(_test) for _test in error_list))


                count += 1


    tests_ran = sorted(tests_ran)
    fail_list = sorted(fail_list)
    logger.info(str(suites_ran) + " Testing has completed")
    logger.info("#" * 75)
    logger.info("Breakdown of tests:")
    logger.info("Tests ran: " + str(count) + "\n" + " " * 12 + ("\n" + " " * 12).join(str(_test) for _test in tests_ran))
    logger.info("Tests passed: " + str(success))
    logger.info("Tests failed: " + str(fail))
    if count == 0:
        logger.info("Pass rate: N/A")
        return
    else:
        logger.info("Pass rate: " + str((success / count) * 100) + "%")
    if fail_list:
        logger.info("List of failed tests:\n" + " " * 12 + ("\n" + " " * 12).join(str(_test) for _test in fail_list))
    logger.info("#" * 75)

    if (success / count) * 100 >= 75:
        return True

    return False


if __name__ == '__main__':


    if sys.argv[1].lower() == "all":
        for suite in TEST_LIST.keys():
            print(TEST_LIST)

            for arg in sys.argv[2:]:
                if 'env' in arg.lower():
                    _test_formatter(suite, **{'env': arg.split('=')[1]})



    else:
        d = {}
        args = sys.argv[2:]
        for i in range(len(args)):
            j = 1
            combine = ''
            if '=' in args[i]:
                #save the key
                key = args[i].split('=')[0]
                try:
                    #check to see if the next value is a kwarg.  If not combine the next args into a string and append to the value
                    #This is to allow spaces in kwargs eg. sheet=this is my sheet
                    while '=' not in args[i+j]:
                        combine = combine + ' ' + args[i+j]
                        j += 1
                except:
                    pass
                value = args[i].split('=')[1] + combine
            d[key] = value.strip("'\\").strip("'")
        _test_formatter(sys.argv[1], **dict(d))

