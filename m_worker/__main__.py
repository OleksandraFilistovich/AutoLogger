import time

from playwright.sync_api import sync_playwright

from utils.rs import Cache
from utils.logs import get_logger

from m_worker.worker import PageHandler, EmailConformation


URL_SIGNUP = "https://opencorporates.com/"
URL_EMAIL = "https://tempail.com/"

LOGGER = get_logger("Worker_main")

cache_0 = Cache(0)



def main():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)

    #  NEW EMAIL
    email_handler = EmailConformation()
    email_address = email_handler.get_email()
    LOGGER.info(f'email created: {email_address}')

    #  SIGN UP INFO
    browser_context = browser.new_context()
    browser_page = browser_context.new_page()

    signup_handler = PageHandler(browser_page)

    signup_handler.go_to_signup()
    signup_handler.input_data(email_address)
    signup_handler.recaptcha()

    #  GET CONFIRMATION LINK
    confirmation_link = email_handler.get_link()
    LOGGER.info(f'Confirmation link: {confirmation_link}')
    browser_page.goto(confirmation_link, wait_until="load", timeout=60000)

    cookies = browser_context.cookies(confirmation_link)
    cache_0.add_results(confirmation_link, cookies)
    LOGGER.info(f'Cookies redis: {cache_0.get_results()}')

    time.sleep(150)

    browser_page.close()

    browser.close()
    playwright.stop()

main()
