import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

EMAIL = os.environ["EMAIL"]
PW = os.environ["PW"]
SIMILAR_ACCOUNT = "chefsteps"


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")

    def find_followers(self):
        pass

    def follow(self):
        pass


insta = InstaFollower()
insta.login()
insta.find_followers()
insta.follow()
