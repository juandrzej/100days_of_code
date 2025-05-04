import requests
from twilio.rest import Client
import random
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.getenv('API_KEY')
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
from_number = os.getenv('FROM_NUMBER')
to_number = os.getenv('TO_NUMBER')
LAT = 59.32
LNG = 9.06

params = {
    "lat": LAT,
    "lon": LNG,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(url=OWM_Endpoint, params=params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for forecast in weather_data["list"]:
    if forecast["weather"][0]["id"] < 700:
        will_rain = True

if will_rain:
    with open("umbrella.txt") as file:
        text = file.read().splitlines()
    sms_text = random.choice(text)
    client = Client(account_sid, auth_token)
    message = (client.messages
    .create(
        body=sms_text,
        from_=from_number,
        to=to_number
    ))
    print(message.status)


