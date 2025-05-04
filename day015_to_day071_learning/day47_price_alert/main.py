import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import smtplib

# Set your target price
TARGET_PRICE = 100

# Load email credentials from .env file
load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# Amazon product URL
URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

# Request headers
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en,pl-PL;q=0.9,pl;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

# Fetch and parse the page
response = requests.get(URL, headers=headers).content
soup = BeautifulSoup(response, "html.parser")

# Extract price
try:
    price = soup.select(".aok-offscreen")[0].getText()
    float_price = float(price.replace("$", ""))
except (AttributeError, ValueError):
    print("Failed to fetch the price. The website's structure may have changed.")
    float_price = None


# Check if price is below target and send an email
if float_price and TARGET_PRICE > float_price:
    try:
        product_name = soup.select("#productTitle")[0].getText()
        formatted_product_name = ' '.join(product_name.split()).replace(" ,", ",")

        email_body = (f"{formatted_product_name} is now ${float_price} \n"
                      f"{URL}")

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject:Amazon Price Alert! \n\n {email_body}".encode("utf-8"))

        print("Price alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
else:
    print("Price is still above the target or unavailable.")
