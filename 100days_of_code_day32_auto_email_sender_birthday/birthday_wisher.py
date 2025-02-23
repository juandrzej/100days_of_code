import os
import smtplib
import random
import datetime as dt
import pandas
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

MY_EMAIL = os.getenv('EMAIL')
MY_PASSWORD = os.getenv('PASSWORD')

data = pandas.read_csv("birthdays.csv")
birthdays_dict = data.to_dict(orient="records")


# 2. Check if today matches a birthday in the birthdays.csv
def check_birth():
    today = (dt.datetime.now().month, dt.datetime.now().day)

    for line in birthdays_dict:
        if (int(line['month']), int(line['day'])) == today:
            return line


person_dict = check_birth()

# 3. If step 2 is true, pick a random letter from letter templates
# and replace the [NAME] with the person's actual name from birthdays.csv
current_number = random.randint(1, 3)
with open(f"letter_templates/letter_{current_number}.txt") as file:
    email_body = file.read().replace('[NAME]', person_dict['name'])


# 4. Send the letter generated in step 3 to that person's email address.
with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL,
                        to_addrs=person_dict['email'],
                        msg=f"Subject: Happy Birthday! \n\n {email_body}")
