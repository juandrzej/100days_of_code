from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Configure WebDriver to keep the browser open and maximize the window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()


# Open LinkedIn job search page
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3985511664&f_"
           "AL=true&geoId=91000000&keywords=sales%20manager&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")

time.sleep(2)


# Sign in to LinkedIn
sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in_button.click()
time.sleep(2)

email_field = driver.find_element(By.ID, "username")
email_field.send_keys(USERNAME)

password_field = driver.find_element(By.ID, "password")
password_field.send_keys(PASSWORD)

login_button = driver.find_element(By.CSS_SELECTOR, ".btn__primary--large.from__button--floating")
login_button.click()
time.sleep(2)


# Reload job search page after login
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3985511664&f_"
           "AL=true&geoId=91000000&keywords=sales%20manager&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true")
time.sleep(4)


# Loop through job listings and apply
jobs = driver.find_elements(By.CSS_SELECTOR,
                            ".disabled.ember-view.job-card-container__link"
                            ".job-card-list__title.job-card-list__title--link")

for job in jobs:
    job.click()
    time.sleep(3)

    try:
        easy_apply_button = driver.find_element(By.CSS_SELECTOR,
                                         ".jobs-apply-button.artdeco-button."
                                         "artdeco-button--3.artdeco-button--primary.ember-view")
        easy_apply_button.click()
        time.sleep(2)

        # Submit the application
        submit_button = driver.find_element(By.CSS_SELECTOR,
                                         ".artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view")
        submit_button.click()

        # Close the Easy Apply modal
        exit_button = driver.find_element(By.CSS_SELECTOR,".artdeco-button__icon")
        exit_button.click()

        # Handle the discard confirmation, if prompted
        try:
            discard_button = driver.find_element(By.CSS_SELECTOR,".artdeco-button.artdeco-button--2.artdeco-button--secondary"
                                                          ".ember-view.artdeco-modal__confirm-dialog-btn")
            discard_button.click()
        except NoSuchElementException:
            pass

    except NoSuchElementException:
        print("Easy Apply button not found for this job. Skipping...")
        continue
