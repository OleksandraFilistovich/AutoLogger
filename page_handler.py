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
   
        self.browser_page.screenshot(path="info.png")
    
    def recaptcha(self) -> None:
        time.sleep(5)
        html_content = self.browser_page.content()
        selector = Selector(text=html_content)

        xpath = '//div[@class="g-recaptcha"]/@data-sitekey'
        site_key = '6LfNR90SAAAAAMjuou-Bhh1HFLoa4BpoZttxz4RL'
        print(site_key)
        
        solver = TwoCaptcha('f35d8c9b68dd7ae711093739a6bcd676')
        result = solver.recaptcha(sitekey=site_key,
                                  url='https://opencorporates.com/users/sign_up')
        print(result['code'])




        captcha_response = self.browser_page.query_selector('.g-recaptcha-response')
        
        self.browser_page.eval_on_selector('.g-recaptcha-response',
                                           f'node => node.value = {result["code"]}')
        time.sleep(10)
        self.browser_page.screenshot(path="captcha.png")

        """
        self.browser_page.mouse.wheel(0, 15000)

        self.browser_page.locator('[value="Register new account"]').click()
        button = self.browser_page.query_selector('.btn-primary')
        button.click()

        xpath = '//label[@id="recaptcha-anchor-label"]/text()'
        cap = selector.xpath(xpath).get()
        print(cap)
        
        self.browser_page.query_selector('name=commit').click()
        time.sleep(5)
        self.browser_page.screenshot(path="captcha.png")
        with recaptchav2.SyncSolver(self.browser_page) as solver:
            print(solver.recaptcha_is_visible())
            token = solver.solve_recaptcha(wait=True)
        """

        


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
    browser = playwright.chromium.launch(headless=False)

    #  EMAIL
    browser_page = browser.new_page()

    #email_handler = EmailConformation(browser_page)
    #email_handler.get_email()

    browser_page.close()

    #  SIGN UP
    browser_page = browser.new_page()

    signup_handler = PageHandler(browser_page)

    signup_handler.go_to_signup()
    signup_handler.input_data('h3elllo@gmail.com')
    signup_handler.recaptcha()

    browser_page.close()

    browser.close()
    playwright.stop()

main()
    

