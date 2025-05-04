from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Constants
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc5Acl3rZH0W2vtlovguiakayH1Vua959-rGoxCAf0li0kIbg/viewform?usp=sf_link"
RENT_URL = "https://appbrewery.github.io/Zillow-Clone/"

# Fetching page HTML
response = requests.get(RENT_URL).text

# Parsing HTML using BeautifulSoup
soup = BeautifulSoup(response, "html.parser")

# Retrieving all real estate links
all_links = [link["href"] for link in soup.find_all(name="a", class_="property-card-link")]

# Retrieving all real estate prices
all_prices = [price.text for price in soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")]
all_prices = [price[:6] if price[2] == "," else price[:2] + "," + price[2:5]
              for price in all_prices]

# Retrieving all real estate addresses
all_addresses = [
    address.text.replace(" | "," ").strip()
    for address in soup.find_all(name="address")
]

# Setting Chrome options to keep the browser open (only for testing purposes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initiating WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Iterating through all property data entries
for i in range(len(all_addresses)):

    # Open the Google Form
    driver.get(GOOGLE_FORM_URL)

    # Locating input fields
    address_field = driver.find_element(
        By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )

    price_field = driver.find_element(
        By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )

    link_field = driver.find_element(
        By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )

    send_form = driver.find_element(
        By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span'
    )

    # waiting for page to load
    time.sleep(2)

    # Filling the form fields
    address_field.send_keys(all_addresses[i])
    price_field.send_keys(all_prices[i])
    link_field.send_keys(all_links[i])

    # Submitting the form
    send_form.click()
