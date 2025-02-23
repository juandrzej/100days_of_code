import requests
import datetime as dt
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

pix_endpoint = "https://pixe.la/v1/users"
username = os.getenv('USERNAME')
token = os.getenv('token')

headers = {
    "X-USER-TOKEN": token
}

user_params = {
    "token": token,
    "username": username,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# user creation
# response = requests.post(url=PIX_ENDPOINT, json=user_params)
# print(response.text)

# graph creation
graph_endpoint = f"{pix_endpoint}/{username}/graphs"

graph_config = {
    "id": "graph1",
    "name": "brz/ska/med/pom",
    "unit": "commit",
    "type": "int",
    "color": "ajisai"
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)


# pixel creation
pixel_endpoint = f"{graph_endpoint}/{graph_config['id']}"

date_now = dt.datetime.now()
date_now_strf = date_now.strftime("%Y%m%d")
print(date_now_strf)

pixel_body = {
    "date": date_now_strf,
    "quantity": "1"
}

# response = requests.post(url=pixel_endpoint, headers=headers, json=pixel_body)
# print(response.text)


# pixel update
update_pixel_endpoint = f"{pixel_endpoint}/{date_now_strf}"

update_pixel_body = {
    "quantity": "3"
}

# response = requests.put(url=update_pixel_endpoint, headers=headers, json=update_pixel_body)
# print(response.text)


# pixel deletion
# response = requests.delete(url=update_pixel_endpoint, headers=headers)
# print(response.text)
