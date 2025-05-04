from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# keep chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.maximize_window()

driver.get("https://tinder.com/app/recs")

time.sleep(2)

logins = driver.find_elements(By.CSS_SELECTOR, ".lxn9zzn")
login = [login for login in logins if login.text == "Log in"]
login[0].click()

time.sleep(2)

google = driver.find_element(By.XPATH, '//*[@id="gsi_992160_625995"]')
google.click()

# phone = driver.find_element(By.XPATH, '//*[@id="s-135409267"]/div/div[1]/div/div[1]/div/div/div[2]/div[2]/span/div[3]/button/div[2]/div[2]/div[2]/div/div')
# phone.click()
#
# time.sleep(2)
