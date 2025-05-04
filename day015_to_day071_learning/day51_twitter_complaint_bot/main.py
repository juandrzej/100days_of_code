import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


# static data; use your internet expected speed and login credentials
PROMISED_DOWN = 300
PROMISED_UP = 50
load_dotenv()
TWITTER_EMAIL = os.environ["TWITTER_EMAIL"]
TWITTER_PW = os.environ["TWITTER_PW"]
TWITTER_LOGIN = os.environ["TWITTER_LOGIN"]

# testing commands so that the browser doesn't close after finishing; need to add options=chrome_options to driver
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)


class InternetSpeedTwitterBot:
    """Twitter bot that checks your download and upload internet speed and makes a complaint on Twitter."""
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        """This function checks your download and upload internet speed."""
        self.driver.get("https://www.speedtest.net/")

        # rejecting cookies
        time.sleep(2)
        cookies = self.driver.find_element(By.ID, "onetrust-reject-all-handler")
        cookies.click()

        # starting speed test
        time.sleep(2)
        go = self.driver.find_element(By.CLASS_NAME, "start-text")
        go.click()

        # closing popup window
        time.sleep(50)
        close = self.driver.find_element(By.LINK_TEXT, "Back to test results")
        close.click()

        # retrieving internet speed values
        time.sleep(2)
        down = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.download-speed")
        up = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.upload-speed")

        # changing values to floats and passing to class variables
        self.down = float(down.text)
        self.up = float(up.text)

    def check_speed(self):
        """This function compares expected speed with real one and runs tweet complainer if needed."""
        if self.down < PROMISED_DOWN or self.up < PROMISED_UP:
            self.tweet_at_provider()

    def tweet_at_provider(self):
        """This function makes a complaint tweet about speed."""

        # message to be posted
        message = (f"Hey Internet Provide, why is my internet speed {self.down}down/{self.up}up"
                   f"when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?")

        self.driver.get("https://twitter.com/home/")

        # passing email to begin logging in
        time.sleep(5)
        sign_in = self.driver.find_element(By.CSS_SELECTOR, ".r-30o5oe.r-1dz5y72")
        sign_in.send_keys(TWITTER_EMAIL)
        sign_in.send_keys(Keys.ENTER)

        # for safety; sometimes you can just give pw, sometimes it will want your login first
        time.sleep(2)
        try:
            password = self.driver.find_element(By.NAME, "password")
        except NoSuchElementException:
            name = self.driver.find_element(By.NAME, "text")
            name.send_keys(TWITTER_LOGIN)
            name.send_keys(Keys.ENTER)
            time.sleep(2)
            password = self.driver.find_element(By.NAME, "password")
        finally:
            password.send_keys(TWITTER_PW)
            password.send_keys(Keys.ENTER)

        # composing a tweet
        time.sleep(6)
        post = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        post.send_keys(message)

        # posting a tweet
        time.sleep(3)
        post_btn = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')
        post_btn.click()


# initiating class
twitter_bot = InternetSpeedTwitterBot()

# running speedtest
twitter_bot.get_internet_speed()

# checking speed values
print(twitter_bot.down)
print(twitter_bot.up)

# running speed check (and twitter complainer if applies)
twitter_bot.check_speed()
