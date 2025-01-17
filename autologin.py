#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import argparse
import os
import sys
import time
import random
import logging

# init logging to stdout and file
logger = logging.getLogger('afraid-autologin')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s >>> %(levelname)s: %(message)s')

file_logger = logging.FileHandler('afraid-autologin.log')
file_logger.setFormatter(formatter)
logger.addHandler(file_logger)

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(formatter)
logger.addHandler(stdout_logger)

logger.debug('afraid-autologin startup')
try:
    from settings import USERNAME, PASSWORD, URL , URL_DORMANT , URL_DORMANT_EXTEND
    if USERNAME == "" or PASSWORD == "":
        raise ImportError
except ImportError:
    logger.error("You need the username and password in the settings.py file:")
    logger.error("USERNAME = 'my_username_here'")
    logger.error("PASSWORD = 'my_password_here'")
    sys.exit(-1)

def main(logger):

    parser = argparse.ArgumentParser(description=' \
        Logs in freedns.afraid.org using USERNAME/PASSWORD from settings.py. \
        Avoids account from being terminated due to inactivity (6 months).\
        Run this script using cron every few months:\
            source bin/activate && python autologin.py')

    parser.add_argument('--browser', default='firefox', help='browser name \
                        must be supported by selenium \
                        (options: firefox, phantomjs')

    parser.add_argument('--verbose', action='store_true',
                        help='show extra output')

    parser.add_argument('--headless', action='store_true', help='initialise a \
                        virtual display for headless systems')

    args = parser.parse_args()

    if args.headless:
        logger.debug('init virtual display')
        from pyvirtualdisplay import Display

        display = Display(visible=0, size=(1366, 768))
        display.start()

    logger.debug('init browser')
    if args.browser == 'phantomjs':
        browser = webdriver.PhantomJS()
    else:
        options = Options()
        options.set_preference("browser.download.folderList", 2)

        browser = webdriver.Firefox(options=options)

    browser.get(URL)
    time.sleep(random.randint(1,3))

    logger.debug('navigating to login page')
    browser.find_element(By.LINK_TEXT, "Main Menu").click()
    time.sleep(random.randint(1,3))

    logger.debug('submit login form')
    username_field = browser.find_element(By.NAME, "username")
    password_field = browser.find_element(By.NAME, "password")
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    browser.find_element(By.NAME, "submit").click()
    time.sleep(random.randint(1,3))
    logger.debug('extending account if dormant')
    # https://freedns.afraid.org/dormant/
    browser.get(URL_DORMANT);

    buttons = browser.find_elements(By.XPATH, "//input[@type='submit']")
    logger.debug(buttons)
    for input in buttons:
        #logger.debug('attribute name of each input element')
        #logger.debug(input.get_attribute('value'))
        if input.get_attribute('value') == "Extend your account":
            input.click()
            break
    # https://freedns.afraid.org/dormant/?action=extend
    browser.get(URL_DORMANT_EXTEND);

    time.sleep(random.randint(1,3))
    # view the subdomains
    browser.find_element(By.LINK_TEXT, "Subdomains").click()

    # check whether login was successful
    # 'Last IP' is only shown after login
    success = 'Last IP' in browser.page_source
    if success:
        logger.info('login sucessful')
    else:
        logger.error('login unsuccessful')

    browser.quit()
    if args.headless:
        display.stop()

    exit_code = 0
    if not success:
        exit_code = -1
    exit(exit_code)

if __name__ == "__main__":
    main(logger)
