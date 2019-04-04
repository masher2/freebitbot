from time import sleep
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException, ElementClickInterceptedException,
    NoSuchElementException
)


class FreebitBot:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get('https://freebitco.in/')

        self.deny_notifications()

        # Login
        self.driver\
            .find_element_by_class_name('login_menu_button')\
            .click()
        self.driver\
            .find_element_by_id('login_form_btc_address')\
            .send_keys('japbogado@gmail.com')

        # Wait for me to login
        sleep(15)

    def deny_notifications(self):
        removed = False
        try:
            self.driver\
                .find_element_by_css_selector('div.pushpad_deny_button')\
                .click()
            removed = True
        except ElementNotInteractableException:
            if not removed:
                self.deny_notifications()

    def deny_multiply_btc(self):
        removed = False
        try:
            self.driver.find_element_by_css_selector(
                '#myModal22.reveal-modal.open > a.close-reveal-modal'
            ).click()
            removed = True
        except ElementNotInteractableException:
            if not removed:
                self.deny_multiply_btc()

    def claim_btc(self):
        self.driver.find_element_by_id('free_play_form_button').click()
        self.deny_multiply_btc()

    def main(self):
        while True:
            try:
                self.claim_btc()
            except ElementNotInteractableException:
                sleep(5)
            except NoSuchElementException:
                sleep(5)
            except ElementClickInterceptedException:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )


if __name__ == '__main__':
    bot = FreebitBot()
    bot.main()
