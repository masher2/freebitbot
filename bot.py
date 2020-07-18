#! /home/masher2/.venvs/freebitbot/bin/python
import logging
import logging.config
import re
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException, ElementClickInterceptedException,
    NoSuchElementException
)


logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
            'datefmt': '%H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
})
logger = logging.getLogger(__name__)


class FreebitBot:

    def __init__(self):
        logger.info('Initializing FreebitBot.')
        self.driver = webdriver.Firefox()
        self.driver.get('https://freebitco.in/')

        self.deny_notifications()

        # Login
        logger.info('Navigating to the loging screen.')
        self.driver\
            .find_element_by_class_name('login_menu_button')\
            .click()
        self.driver\
            .find_element_by_id('login_form_btc_address')\
            .send_keys('japbogado@gmail.com')

        logger.info('Wating for the user to log in.')
        self.wait_for_login()

    def wait_for_login(self):
        try:
            self.driver.find_element_by_id('login_form_btc_address')
            sleep(5)
            self.wait_for_login()
        except NoSuchElementException:
            logger.info('Successfully logged')

    def deny_notifications(self):
        logger.info('Removing the notification popup')
        try:
            self.driver\
                .find_element_by_css_selector('div.pushpad_deny_button')\
                .click()
            logger.info('Removed the pop up')
        except ElementNotInteractableException:
            logger.error('Could not remove the notification popup')
        except Exception as e:
            logger.error(f"Unexpected error, retrying.\nThe exception was: {e}")

    def claim_btc(self):
        try:
            logger.info('Trying to claim the btc.')
            self.driver.find_element_by_id('free_play_form_button').click()
            sleep(5)
            logger.info('BTC Claimed!')
        except Exception:
            sleep(5)

    def check(self):
        """ Checks if can claim the BTC

        Returns False if not ready to claim, True otherwise
        """
        try:
            # No internet
            if self.driver.title == 'Server Not Found':
                self.driver.refresh()
                return False

            # Stopped clock
            if re.search('^0m\:0s', self.driver.title):
                self.driver.refresh()
                return False

            # Waiting
            if re.search('^\d{1,2}m\:\d{1,2}s', self.driver.title):
                return False

            # Notification popup
            if self.driver.find_element_by_css_selector('div.pushpad_deny_button').is_displayed():
                self.deny_notifications()
                return False

            # Are we ready?
            ready = self.driver.find_element_by_id('free_play_form_button').is_displayed()
            if ready:
                # Scrolling to bottom
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
            return ready

        except Exception:
            return False

    def main(self):
        while True:
            if self.check():
                self.claim_btc()
            else:
                sleep(10)


if __name__ == '__main__':
    bot = FreebitBot()
    bot.main()
