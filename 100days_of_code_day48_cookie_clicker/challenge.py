from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

driver.get("https://secure-retreat-92358.herokuapp.com/")

fname = driver.find_element(By.NAME, "fName")
fname.send_keys("firstname")

lname = driver.find_element(By.NAME, "lName")
lname.send_keys("lastname")

emailo = driver.find_element(By.NAME, "email")
emailo.send_keys("emailo@gmail.com")

button = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
button.click()
