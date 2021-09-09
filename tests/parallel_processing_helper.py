import pandas
import time
import setup_functions
import sys

from selenium import webdriver
from webdriverwrapper import Chrome
from webdriverwrapper import Remote
from tests.architecture import common_functions
from parsing import get_functions
from time import sleep
from filelock import Timeout, FileLock


def _bulk_process(logger, excel_file, excel_data, sheet, write_column, function, function_args, environment, performance_mode, session_id, executor_url):
    '''
        This function is the workhorse for bulk_parallel_process.  Do not call this function by itself.
    '''

    start_time = time.time()


    validation_results = []
    cdcs = []
    for item in excel_data:
        fail_count = 0
        try:
            if item[1]['result'] != "error" and item[1]['result'] != "":
                cdcs.append(item[1]['result'])
                continue
        except:
            pass
        while True:
            if fail_count >= 2:
                logger.info("Failed two times. Skipping")
                cdcs.append("error")
                break
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                driver2 = Remote(command_executor=executor_url, options=chrome_options)
                #driver2.session_id = session_id
                #driver = setup_functions.setup_driver(logger, str(function), performance_mode=performance_mode)
                # Every function will need a data arg so this function can pass the excel data.
                result = eval(get_functions(logger, function) + "(driver2, logger, env='"+ str(environment) + "', data="+str(item[1])+")")
                try:
                    cdcs.append(result["cdcs_number"])
                except:
                    cdcs.append(result)
                driver2.close()
                break

            except Exception as e:
                logger.info(e)
                if 'Max retries exceeded' in str(e):
                    continue
                if 'Connection refused' in str(e):
                    continue
                if 'invalid session id' in str(e):
                    continue
                fail_count += 1
                try:
                    driver2.close()
                except:
                    pass
                logger.info("fail count: " + str(fail_count))
                sleep(30)


    print("This is cdcs")
    print(cdcs)

    if excel_data[0][0] <= 2:
        cdcs_data = {"result": cdcs}
        lock = FileLock(excel_file + ".lock")
        with lock:
            common_functions.write_to_excel(excel_file, pandas.DataFrame(cdcs_data), logger, sheet_name=sheet, startrow=0, startcol=write_column, index=False)
    else:
        cdcs_data = {"": cdcs}
        lock = FileLock(excel_file + ".lock")
        with lock:
            common_functions.write_to_excel(excel_file, pandas.DataFrame(cdcs_data), logger, sheet_name=sheet, startrow=excel_data[0][0] - 1, startcol=write_column, index=False, header=False)


    logger.info("--- Thread took %s seconds to process ---" % (time.time() - start_time))


if __name__ == '__main__':
    logger = setup_functions.setup_logger()
    globals()[sys.argv[1]](logger)
