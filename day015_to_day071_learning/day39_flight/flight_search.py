import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
ORIGIN_CITY = "LON"

MAX_DAYS_SEARCH = 4
VACATION_LENGTH_DAYS = 1

class FlightSearch:
    """This class is responsible for talking to the Flight Search API."""

    def __init__(self, sheet_data):
        self.sheet_data = sheet_data
        self.api_key = os.environ["AMADEUS_API_KEY"]
        self.api_secret = os.environ["AMADEUS_SECRET"]
        self.headers = {}
        self.dates = {}
        self.departure_date = ""
        self.return_date = ""

    def access_token(self):
        """ This function gets the valid token. """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }

        response = requests.post(url=TOKEN_ENDPOINT, headers=headers, data=data)
        return response.json()

    def find_dates(self):
        """ This function finds current dates and saves them as strings."""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        six_months_later = today + timedelta(days=183)
        self.departure_date = tomorrow.strftime("%Y-%m-%d")
        self.return_date = six_months_later.strftime("%Y-%m-%d")

        for n in range(1, MAX_DAYS_SEARCH + 1):
            dep_date = today + timedelta(days=n)

            self.dates[dep_date.strftime("%Y-%m-%d")] = []

            for m in range(1, VACATION_LENGTH_DAYS + 1):
                ret_date = dep_date + timedelta(days=m)

                self.dates[dep_date.strftime("%Y-%m-%d")].append(ret_date.strftime("%Y-%m-%d"))

        print(self.dates)

    def find_flights(self):
        """ This function finds flight deals thru API."""
        self.find_dates()
        data = {}

        for destination in self.sheet_data:
            data[f"{destination['city']}"] = []

            for departure_date in self.dates:
                for return_date in departure_date:
                    params = {
                        "originLocationCode": ORIGIN_CITY,
                        "destinationLocationCode": destination["iataCode"],
                        "departureDate": departure_date,
                        "returnDate": return_date,
                        "adults": 1,
                        "nonStop": 'true',
                        "maxPrice": destination["lowestPrice"],
                        "max": 10
                    }

                    # safety loop for outdated token
                    error = True
                    while error:
                        response = requests.get(url=FLIGHT_ENDPOINT, headers=self.headers, params=params)
                        print(response.json())
                        try:
                            if response.json()["data"]:
                                data[f"{destination['city']}"].append(response.json()["data"])
                        except KeyError:
                            self.update_token()
                            error = True
                        else:
                            error = False

        return data

    def update_token(self):
        """ This function updates outdated token to valid one."""
        token = self.access_token()['access_token']
        self.headers = {
            "Authorization": f"Bearer {token}"
        }
