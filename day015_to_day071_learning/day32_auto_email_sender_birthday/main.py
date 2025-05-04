import os
import smtplib
import datetime as dt
import random
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


with open("quotes.txt") as file:
    quotes_list = file.read().splitlines()

day_of_week = dt.datetime.now().weekday()

ran_quot = random.choice(quotes_list)

with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(
        from_addr=email,
        to_addrs=email,
        msg=f"Subject:Hello \n\n {ran_quot}")