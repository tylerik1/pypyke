'''
Created on Dec 10, 2019

@author: erik.kniaz
'''

from tests.architecture.add_to_cart import helpers
import common_functions
import sys
from decorators import unit,smoke,regression,functional

@smoke
@regression
def add_first_toaster_to_cart(logger):
    driver = common_functions.setup_driver(logger, "add_first_toaster_to_cart")
    
    driver.get("https://www.amazon.com")
    
    common_functions.make_screenshot(driver, "amazon_home_page", logger)
    
    helpers.search_for_item(driver, logger, "toaster")
    
    helpers.select_item(driver, 0, logger)

    helpers.add_to_cart(driver, logger)

@regression
def add_second_toothbrush_to_cart(logger):
    driver = common_functions.setup_driver(logger, "add_second_toothbrush_to_cart")
    
    driver.get("https://www.amazon.com")
    
    common_functions.make_screenshot(driver, "amazon_home_page", logger)
    
    helpers.search_for_item(driver, logger, "toothbrush")
    
    helpers.select_item(driver, 1, logger)

    helpers.add_to_cart(driver, logger)


if __name__ == '__main__':
    logger = common_functions.setup_logger()
    #add_second_toothbrush_to_cart(logger)
    globals()[sys.argv[1]](logger)