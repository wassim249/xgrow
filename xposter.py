import pickle
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service

class XPoster:
    _options = webdriver.FirefoxOptions()
    _options.add_argument('--headless')

    driver = webdriver.Firefox(options=_options, service=Service("./driver/geckodriver"))
    server_started = False
    instance = None

    def __init__(self, username, password) -> None:
        if XPoster.instance is None:
            XPoster.instance = self
        self.username = username
        self.password = password

        if not XPoster.server_started:
            self.start_server()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(XPoster, cls).__new__(cls)
        return cls.instance

    def start_server(self):
        self._signin()
        XPoster.server_started = True

    @staticmethod
    def close_server():
        XPoster.driver.quit()
        XPoster.server_started = False

    def _signin(self):
        XPoster.driver.get("https://twitter.com/login")
        while True:
            try:
                username_input = XPoster.driver.find_element(By.TAG_NAME, 'input')
                username_input.send_keys(self.username)
                break
            except:
                sleep(1)
        username_input.send_keys(Keys.ENTER)
        while True:
            try:
                password_input = XPoster.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
                self.slow_typing(password_input, self.password)
                break
            except:
                sleep(1)
        password_input.send_keys(Keys.ENTER)

    def post_tweet(self, tweet: str, img: str = None) -> str:
        if not XPoster.server_started:
            self.start_server()

        if len(tweet) > 280:
            return "Cannot post the tweet, the tweet length should be less than or equal to 280 characters"
        while True:
            try:
                tweet_input = XPoster.driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
                tweet_input.click()
                self.slow_typing(tweet_input, tweet + " ")
                break
            except Exception as e:
                sleep(0.2)
        if img:
            XPoster.driver.find_element(By.CSS_SELECTOR, 'input[data-testid="fileInput"]').send_keys(img)
        sleep(2)
        while True:
            try:
                post_button = XPoster.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButtonInline"]')
                # check if the tweet button is disabled
                if post_button.get_attribute('aria-disabled') == 'true':
                    # clear the tweet input
                    tweet_input.send_keys(Keys.CONTROL + "a")
                    tweet_input.send_keys(Keys.DELETE)
                    try:
                        remove_button = XPoster.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Remove media"]')
                        remove_button.click()
                    except NoSuchElementException:
                        print("Remove media button does not exist.")

                    return "Cannot post the tweet,check the tweet length"
                post_button.click()
                break
            except Exception as e:
                sleep(0.1)
        return tweet

    @staticmethod
    def slow_typing(element, text):
        for character in text:
            element.send_keys(character)
            sleep(0.05)