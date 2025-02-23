import requests
from datetime import datetime
import smtplib
import time

from config import MY_LAT, MY_LONG, MY_PASSWORD, MY_EMAIL


def is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.
    lat_check = MY_LAT - iss_latitude
    lng_check = MY_LONG - iss_longitude
    if 5 > lat_check > -5:
        if 5 > lng_check > -5:
            return True
    return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 2
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 2

    hour_now = datetime.now().hour
    if sunset >= hour_now >= sunrise:
        return False
    return True

# If the ISS is close to my current position
# and it is currently dark
# Then email me to tell me to look up.
# BONUS: run the code every 60 seconds.


while True:
    time.sleep(60)
    if is_close() and is_dark():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg="Subject: Look up now!")

