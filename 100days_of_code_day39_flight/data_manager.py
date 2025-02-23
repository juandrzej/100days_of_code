import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/00f653c028ac6f75dab737786cb8904c/flightDeals/prices"


class DataManager:
    """This class is responsible for talking to the Google Sheet."""

    def __init__(self):
        self.user = os.environ["SHEETY_USRERNAME"]
        self.password = os.environ["SHEETY_PASSWORD"]
        self.authorization = HTTPBasicAuth(self.user, self.password)
        self.flights_data = {}

    def get_flights_data(self):
        """Use the Sheety API to GET all the data in that sheet and print it out."""
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self.authorization)
        data = response.json()
        self.flights_data = data["prices"]
        return self.flights_data


