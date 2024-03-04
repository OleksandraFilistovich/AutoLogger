import time
import string

from mailtm import Email
from random import choice

from parsel import Selector
from playwright.sync_api import sync_playwright, Page

#from playwright_recaptcha import recaptchav2
from twocaptcha import TwoCaptcha


URL_SIGNUP = "https://opencorporates.com/"
URL_EMAIL = "https://tempail.com/"

class PageHandler:
    """Class for scrapping used cars info. Synchronous."""

    def __init__(self, browser_page: Page) -> None:
        self.browser_page = browser_page

    def go_to_signup(self) -> None:
        print('page go')
        self.browser_page.goto(URL_SIGNUP, wait_until="load", timeout=60000)
        self.browser_page.screenshot(path="go_to.png", full_page=True)
        print('button search')

        button = self.browser_page.get_by_role('link')
        button.get_by_text('Login').click()

        self.browser_page.screenshot(path="go_to.png", full_page=True)
        button = self.browser_page.get_by_role('link')
        button.get_by_text('Create an account').click()

    def input_data(self, email: str) -> None:
        self.browser_page.wait_for_url('https://opencorporates.com/users/sign_up')
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
   
        self.browser_page.screenshot(path="info.png")


    def recaptcha(self) -> None:
        time.sleep(5)
        html_content = self.browser_page.content()
        selector = Selector(text=html_content)

        xpath = '//div[@class="g-recaptcha "]/@data-sitekey'
        site_key = selector.xpath(xpath).get()

        print(site_key)
        
        captcha_frame = self.browser_page.wait_for_selector('iframe[src*="recaptcha/api2"]')
        captcha_frame_content = captcha_frame.content_frame()
        captcha_checkbox = captcha_frame_content.wait_for_selector('#recaptcha-anchor')
        captcha_checkbox.click()


        solver = TwoCaptcha('f35d8c9b68dd7ae711093739a6bcd676')
        result = solver.recaptcha(sitekey=site_key,
                                  url='https://opencorporates.com/users/sign_up')
        captcha_response = result['code']
        print(captcha_response)

        
        self.browser_page.eval_on_selector('#g-recaptcha-response',
                                           'el => el.removeAttribute("style")')
        
        self.browser_page.fill('#g-recaptcha-response', captcha_response)
        self.browser_page.mouse.click(1,1)

        self.browser_page.wait_for_selector('input[type="submit"]').click(force=True)
        self.browser_page.wait_for_selector('input[type="submit"]').click()


class EmailConformation:
    def __init__(self) -> None:
        self.email = Email()
        self.link = None

    def get_email(self) -> str:

        self.email.register()
        return self.email.address
    
    def get_link(self) -> str:
        def listener(message):
            if message['text']:
                text = message['text']
                self.link = text[text.index('<')+1:text.index('>')]
            
        self.email.start(listener)
        print("\nWaiting for new emails...")

        while not self.link:
            time.sleep(0.5)
        else:
            self.email.stop()
        return self.link


def main():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)

    #  NEW EMAIL
    email_handler = EmailConformation()
    email_address = email_handler.get_email()
    print(email_address)

    #  SIGN UP INFO
    browser_context = browser.new_context()
    browser_page = browser_context.new_page()

    signup_handler = PageHandler(browser_page)

    signup_handler.go_to_signup()
    signup_handler.input_data(email_address)
    signup_handler.recaptcha()

    #  GET CONFIRMATION LINK
    confirmation_link = email_handler.get_link()
    print(confirmation_link)
    browser_page.goto(confirmation_link, wait_until="load", timeout=60000)

    print(browser_context.cookies(confirmation_link))

    time.sleep(150)

    browser_page.close()

    browser.close()
    playwright.stop()

main()
