# pylint: disable=bare-except,anomalous-backslash-in-string,len-as-condition,too-many-branches
'''
Created on Feb 15, 2019

@author: erik.kniaz
'''
import datetime
import logging
import os.path
import platform
import sys
from pathlib import Path
from time import sleep

from selenium import webdriver
from webdriverwrapper import Chrome


def setup_logger():
    '''
    Sets up a logger object
    '''
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    if platform.system() == "Linux":
        my_file = Path('pypyke/logs/testing.log')
        if my_file.exists():
            file_handler = logging.FileHandler('pypyke/logs/testing.log')
        else:
            os.makedirs(os.path.dirname('pypyke/logs/testing.log'))
            file_handler = logging.FileHandler('pypyke/logs/testing.log')
    if platform.system() == "Windows":
        current = os.getcwd()
        # if we are not in the python base directory then go to it
        while "pypyke\\" in str(current):
            current = Path(current).parent
        my_file = Path(os.path.join(current, "logs", "testing.log"))
        if my_file.exists():
            file_handler = logging.FileHandler(os.path.join(current, "logs", "testing.log"))
        else:
            try:
                os.makedirs(os.path.dirname(os.path.join(current, "logs", "testing.log")))
            except:
                pass
            file_handler = logging.FileHandler(os.path.join(current, "logs", "testing.log"))

    file_handler.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)-10s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def setup_driver(logger, name=None, performance_mode=False):
    '''
    Configures the Chrome driver to run on Jenkins or Windows.
    Also creates and sets the screenshot path
    '''
    date = datetime.datetime.now()
    date = str(date).replace(':', '_').replace('.', '_')
    current = None

    if platform.system() == "Linux":
        my_file = Path("pypyke/screenshots/")
        if my_file.exists():
            os.mkdir(os.path.join("pypyke/screenshots/", name + "_" + date))
            screenshot_path = os.path.join("pypyke/screenshots/", name + "_" + date)
        else:
            os.mkdir("pypyke/screenshots/")
            os.mkdir(os.path.join("pypyke/screenshots/", name + "_" + date))
            screenshot_path = os.path.join("pypyke/screenshots/", name + "_" + date)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        logger.info("detected Linux OS")
    if platform.system() == "Windows":
        current = os.getcwd()
        # if we are not in the python base directory then go to it
        while "pypyke\\" in str(current):
            current = Path(current).parent
        my_file = Path(os.path.join(current, "screenshots"))
        if my_file.exists():
            try:
                os.mkdir(os.path.join(current, "screenshots", name + "_" + date))
            except:
                sleep(1)
                date = datetime.datetime.now()
                date = str(date).replace(':', '_').replace('.', '_')
                os.mkdir(os.path.join(current, "screenshots", name + "_" + date))
            screenshot_path = os.path.join(current, "screenshots", name + "_" + date)
        else:
            try:
                os.mkdir(os.path.join(current, "screenshots"))
                os.mkdir(os.path.join(current, "screenshots", name + "_" + date))
            except:
                sleep(1)
                date = datetime.datetime.now()
                date = str(date).replace(':', '_').replace('.', '_')
                os.mkdir(os.path.join(current, "screenshots"))
                os.mkdir(os.path.join(current, "screenshots", name + "_" + date))
            screenshot_path = os.path.join(current, "screenshots", name + "_" + date)

        if performance_mode:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_experimental_option('useAutomationExtension', False)
        else:
            chrome_options = webdriver.ChromeOptions()
            #chrome_options.add_argument('--no-sandbox')
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--window-size=1920,1080')
        logger.info("detected Windows OS")

    if current:
        driver = Chrome(str(current) + "\\chromedriver.exe", chrome_options=chrome_options)
    else:
        driver = Chrome("chromedriver", chrome_options=chrome_options)

    driver.screenshot_path = screenshot_path
    logger.info("driver object has been created.")
    return driver



def make_screenshot(driver, description, logger):
    '''
    Takes a screenshot with timestamp
    :param driver: driver to control browser
    :param description: description of screenshot
    :return: Takes a screenshot
    '''
    date = datetime.datetime.now()
    date = str(date).replace(' ', '_').replace('.', '').replace(':', '').replace('-', '')
    driver.make_screenshot(date + '_' + description)
    logger.info("screenshot taken")


if __name__ == '__main__':
    globals()[sys.argv[1]]()
