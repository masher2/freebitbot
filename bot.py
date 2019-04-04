import logging
import logging.config
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
    title = 'FreeBitco.in - Bitcoin, Bitcoin Price, Free Bitcoin Wallet, Faucet, Lottery and Dice!'

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

    def deny_notifications(self, previous_call=False):
        if not previous_call:
            logger.info('Looking for the notification pop up.')
            removed = False
            try:
                self.driver\
                    .find_element_by_css_selector('div.pushpad_deny_button')\
                    .click()
                removed = True
            except ElementNotInteractableException:
                logger.error('Could not click the element, retrying.')
                sleep(2)
            except Exception as e:
                logger.error(f"Unexpected error, retrying.\n"
                             f"The exception was: {e}")
            self.deny_notifications(removed)
        else:
            logger.info('Removed the pop up')

    def deny_multiply_btc(self, previous_call=False):
        if not previous_call:
            logger.info('Looking for the multiply btc pop up.')
            removed = False
            try:
                self.driver.find_element_by_css_selector(
                    '#myModal22.reveal-modal.open > a.close-reveal-modal'
                ).click()
                removed = True
            except NoSuchElementException:
                logger.error('Could not click the element, retrying.')
                sleep(2)
            except Exception as e:
                logger.error(f"Unexpected error, retrying.\n"
                             f"The exception was: {e}")
                sleep(2)
            self.deny_multiply_btc(removed)
        else:
            logger.info('Removed the pop up')

    def claim_btc(self):
        logger.info('Trying to claim the btc.')
        able_to_click = self.driver.title == self.title
        if able_to_click:
            while able_to_click:
                self.driver.find_element_by_id('free_play_form_button').click()
                sleep(2)
                able_to_click = self.driver.title == self.title
            logger.info('BTC Claimed!')
            self.deny_multiply_btc()
        else:
            logger.info('Trying again in a minute.')
            sleep(60)

    def main(self):
        logger.info('Initializing main loop.')
        while True:
            try:
                self.claim_btc()
            except ElementNotInteractableException:
                sleep(5)
            except NoSuchElementException:
                sleep(5)
            except ElementClickInterceptedException:
                logger.info('Scrolling to bottom.')
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )


if __name__ == '__main__':
    bot = FreebitBot()
    bot.main()
