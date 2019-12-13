'''
Created on Dec 10, 2019

@author: erik.kniaz
'''
import sys
from time import sleep
import common_functions
from selenium.webdriver.common.keys import Keys



def search_for_item(driver, logger, item_name=None):

    logger.info("searching for item: " + item_name)
    
    driver.get_elm(name='field-keywords').send_keys(item_name, Keys.ENTER)
    
    logger.info("item found!")
    
    common_functions.make_screenshot(driver, "list_of_toasters", logger)
    

def select_item(driver, list_id, logger):

    logger.info("clicking on item")
    
    driver.get_elm(xpath="//img[@data-image-index='"+str(list_id)+"']").click()
    
    logger.info("items page loaded!")
    
    common_functions.make_screenshot(driver, "selected_toaster", logger)


def add_to_cart(driver, logger):
    
    logger.info("adding item to cart")
    
    driver.get_elm(id_='add-to-cart-button').click()
    
    logger.info("item successfully added to cart!")
    
    common_functions.make_screenshot(driver, "added_to_cart", logger)
    

if __name__ == '__main__':
    logger = common_functions.setup_logger()
    search_for_item(logger, "toaster")
    globals()[sys.argv[1]](logger)