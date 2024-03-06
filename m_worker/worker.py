import time
import string

from mailtm import Email
from random import choice

from parsel import Selector
from playwright.sync_api import Page

from twocaptcha import TwoCaptcha

from utils.rs import Cache
from utils.logs import get_logger


URL_SIGNUP = "https://opencorporates.com/"
URL_EMAIL = "https://tempail.com/"

LOGGER = get_logger("Worker")

cache_0 = Cache(0)

class PageHandler:
    """Class for handling sign up pages. Synchronous."""

    def __init__(self, browser_page: Page) -> None:
        self.browser_page = browser_page

    def go_to_signup(self) -> None:
        """Go from home page to sign up one."""
        LOGGER.info('Go to registration page')
        self.browser_page.goto(URL_SIGNUP, wait_until="load", timeout=60000)

        button = self.browser_page.get_by_role('link')
        button.get_by_text('Login').click()

        button = self.browser_page.get_by_role('link')
        button.get_by_text('Create an account').click()

    def input_data(self, email: str) -> None:
        """Input registration data."""
        LOGGER.info('Start input data')
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
        check = self.browser_page.wait_for_selector('.terms-conditions-checkbox')
        self.browser_page.eval_on_selector('.terms-conditions-checkbox',
                                           'el => el.removeAttribute("disabled")')
        check.check()


    def recaptcha(self) -> None:
        """reCaptcha v2 and submit."""
        time.sleep(5)
        html_content = self.browser_page.content()
        selector = Selector(text=html_content)

        xpath = '//div[@class="g-recaptcha "]/@data-sitekey'
        site_key = selector.xpath(xpath).get()

        LOGGER.info(f'Site key: {site_key}')
        
        captcha_frame = self.browser_page.wait_for_selector('iframe[src*="recaptcha/api2"]')
        captcha_frame_content = captcha_frame.content_frame()
        captcha_checkbox = captcha_frame_content.wait_for_selector('#recaptcha-anchor')
        captcha_checkbox.click()


        solver = TwoCaptcha('f35d8c9b68dd7ae711093739a6bcd676')
        result = solver.recaptcha(sitekey=site_key,
                                  url='https://opencorporates.com/users/sign_up')
        captcha_response = result['code']
        
        self.browser_page.eval_on_selector('#g-recaptcha-response',
                                           'el => el.removeAttribute("style")')
        
        self.browser_page.fill('#g-recaptcha-response', captcha_response)
        self.browser_page.mouse.click(1,1)

        self.browser_page.wait_for_selector('input[type="submit"]').click(force=True)
        self.browser_page.wait_for_selector('input[type="submit"]').click()
        LOGGER.info('Captcha solved')


class EmailConformation:
    """Class for handling temporary email."""
    def __init__(self) -> None:
        self.email = Email()
        self.link = None

    def get_email(self) -> str:
        """Get new adress."""
        self.email.register()
        return self.email.address
    
    def get_link(self) -> str:
        """Listens to emails and saves confirmation link."""
        def listener(message):
            if message['text']:
                text = message['text']
                self.link = text[text.index('<')+1:text.index('>')]
            
        self.email.start(listener)
        LOGGER.info('Waiting for new emails...')

        while not self.link:
            time.sleep(0.5)
        else:
            self.email.stop()
        return self.link
