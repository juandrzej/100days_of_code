from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

upgrade_names = ["Time machine", "Portal", "Alchemy lab", "Shipment", "Mine", "Factory", "Grandma", "Cursor"]


def find_upgrades():
    upgrades = {}
    for name in upgrade_names:
        element = driver.find_element(By.ID, value=f"buy{name}")
        price = int(driver.find_element(By.CSS_SELECTOR, value=f"#buy{name.replace(' ', '\ ')} b")
                    .text.split("-")[1].strip().replace(",", ""))
        upgrades[price] = element

    return upgrades


def check_balance():
    money_element = driver.find_element(by=By.ID, value="money").text
    if "," in money_element:
        money_element = money_element.replace(",", "")
    return int(money_element)


game_timeout = time.time() + 60*0.5
buy_timeout = time.time() + 5

while True:
    cookie.click()

    if time.time() > buy_timeout:

        upgrades_dict = find_upgrades()

        for key in upgrades_dict:
            money = check_balance()
            if money > key:
                upgrades_dict[key].click()
                break

        buy_timeout = time.time() + 5

    if time.time() > game_timeout:
        cookie_per_s = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_s)
        break
