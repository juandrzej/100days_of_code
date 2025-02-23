import requests
from datetime import datetime
# from requests.auth import HTTPBasicAuth
import os

GENDER = "male"
WEIGHT_KG = 62
HEIGHT_CM = 184
AGE = 28

NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
NUTRITIONIX_APP_KEY = os.environ.get("NUTRITIONIX_APP_KEY")
NUTRITIONIX_ENDPOINT = os.environ.get("NUTRITIONIX_ENDPOINT")

SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")


def add_exercise_done():
    exercise_text = input("Tell me which exercises you did: ")

    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY
    }
    params = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }
    response = requests.post(url=NUTRITIONIX_ENDPOINT, headers=headers, json=params)
    data = response.json()
    return data


def get_sheets_data():
    # basic = HTTPBasicAuth('test1', 'test2')
    headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
    response = requests.get(url=SHEETY_ENDPOINT, headers=headers)
    data = response.json()
    return data


def add_exercise_done_sheets(data):
    # basic = HTTPBasicAuth('test1', 'test2')
    headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
    now = datetime.now()
    hour_now = now.strftime("%X")
    date_now = now.strftime("%d/%m/%Y")

    for exercise in data["exercises"]:
        body = {
            "workout": {
                "date": date_now,
                "time": hour_now,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"],
            }
        }
        response = requests.post(url=SHEETY_ENDPOINT, json=body, headers=headers)
        print(response.text)


nut_data = add_exercise_done()
add_exercise_done_sheets(nut_data)
sheets_data = get_sheets_data()
print(nut_data)
print(sheets_data)

