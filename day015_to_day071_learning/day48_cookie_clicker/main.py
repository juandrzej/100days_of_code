from selenium import webdriver
from selenium.webdriver.common.by import By

# keep chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.python.org/")

# price_dollar = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_cents = driver.find_element(By.CLASS_NAME, value="a-price-fraction")
#
# print(f"The price is {price_dollar.text}.{price_cents.text}")

# search_bar = driver.find_element(By.NAME, value="q")
# print(search_bar.get_attribute("placeholder"))
#
# button = driver.find_element(By.ID, value="submit")
# print(button.size)
#
# documentation_link = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
# print(documentation_link.text)
#
# bug_link = driver.find_element(By.XPATH, '//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
# print(bug_link.text)

times = driver.find_elements(By.CSS_SELECTOR, value=".medium-widget.event-widget.last time")
events = driver.find_elements(By.CSS_SELECTOR, value=".medium-widget.event-widget.last li a")

my_dict = {}
# print(event.get_attribute("datetime")[:10])
# print(event.text)

for number in range(len(events)):
    my_dict[number] = {
        "time": times[number].get_attribute("datetime")[:10],
        "name": events[number].text
    }

print(my_dict)


# closes one tab
# driver.close()

# closes whole browser
driver.quit()
