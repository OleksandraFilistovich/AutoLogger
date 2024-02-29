import time
import string
import asyncio
from mailtm import Email
from random import choice

from parsel import Selector
from playwright.sync_api import sync_playwright, Page
#from playwright.async_api import Page



URL_SIGNUP = "https://opencorporates.com/"
URL_EMAIL = "https://tempail.com/"

class PageHandler:
    """Class for scrapping used cars info. Synchronous."""

    def __init__(self, browser_page: Page) -> None:
        self.browser_page = browser_page

    def go_to_signup(self) -> None:
        print('page go')
        self.browser_page.goto(URL_SIGNUP, wait_until="load", timeout=60000)
        print('button search')

        button = self.browser_page.get_by_role('link')
        button.get_by_text('Login').click()

        button = self.browser_page.get_by_role('link')
        button.get_by_text('Create an account').click()

    def input_data(self, email: str) -> None:
        name = email[:email.index('@')]

        letters = string.ascii_lowercase
        job = ''.join(choice(letters) for i in range(10))
        company = ''.join(choice(letters) for i in range(8))

        self.browser_page.fill('#user_name', name)
        self.browser_page.fill('#user_email', email)

        self.browser_page.fill('#user_user_info_job_title', job)
        self.browser_page.fill('#user_user_info_company', company)

        self.browser_page.fill('#user_password', name)
        self.browser_page.fill('#user_password_confirmation', name)

        #  Checkbox anabled by changing attributes
        check = self.browser_page.query_selector('.terms-conditions-checkbox')
        self.browser_page.eval_on_selector('.terms-conditions-checkbox',
                                           'el => el.removeAttribute("disabled")')
        check.check()

        #  CheckBox anabled by scrolling
        """
        self.browser_page.query_selector('.terms-conditions-box').hover()
        self.browser_page.mouse.wheel(0, 15000)

        check = self.browser_page.query_selector('.terms-conditions-checkbox')
        time.sleep(0.1)

        if check.is_enabled():
            check.check()
        else:
            time.sleep(0.5)
            print('sleep')
            check.check()
        """

        
        self.browser_page.screenshot(path="ss.png", full_page=True)


class EmailConformation:
    def __init__(self, browser_page: Page) -> None:
        self.browser_page = browser_page
    
    def get_email_(self) -> str:
        print('page go')
        time.sleep(10)
        self.browser_page.goto(URL_EMAIL, wait_until="load", timeout=60000)

        html_content = self.browser_page.content()
        selector = Selector(text=html_content)

        xpath = '//input[@class="adres-input"]/@value'
        email = selector.xpath(xpath).get()

        self.browser_page.screenshot(path="email.png", full_page=True)

        return email
    
    def get_email(self) -> str:
        def listener(message):
            print("\nSubject: " + message['subject'])
            print("Content: " + message['text'] if message['text'] else message['html'])
        test = Email()
        print(f'Domain: {test.domain}')
        test.register()
        print(f'"Email Adress: {str(test.address)}')
        test.start(listener)
        print("\nWaiting for new emails...")



def main():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)

    #  EMAIL
    browser_page = browser.new_page()

    email_handler = EmailConformation(browser_page)
    email_handler.get_email()

    browser_page.close()

    #  SIGN UP
    browser_page = browser.new_page()

    #signup_handler = PageHandler(browser_page)
    #signup_handler.go_to_signup()
    #signup_handler.input_data('abc@gmail.com')

    browser_page.close()

    browser.close()
    playwright.stop()

main()