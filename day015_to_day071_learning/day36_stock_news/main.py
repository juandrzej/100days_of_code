import requests
import datetime as dt
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
api_key_av = os.getenv('API_KEY_AV')
api_key_news = os.getenv('API_KEY_NEWS')
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('auth_token')
from_number = os.getenv('FROM_NUMBER')
to_number = os.getenv('TO_NUMBER')

date_now = dt.datetime.now().date()
y_date = date_now - dt.timedelta(days=1)
dby_date = y_date - dt.timedelta(days=1)
y_date_str = y_date.strftime("%Y-%m-%d")
dby_date_str = dby_date.strftime("%Y-%m-%d")


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def stock_price_check():
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": api_key_av
    }
    response = requests.get(url="https://www.alphavantage.co/query", params=params)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    print(data)
    y_data = float(data[y_date_str]["4. close"])
    dby_data = float(data[dby_date_str]["4. close"])
    print(y_data)
    print(dby_data)
    alarm_diff = y_data * 5/100
    stock_diff = y_data - dby_data
    if alarm_diff < stock_diff or -alarm_diff > stock_diff:
        print("get news")
        stock_difference_percentage = stock_diff / dby_data * 100
        send_sms(stock_difference_percentage)



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
def get_news():
    params = {
        "q": COMPANY_NAME,
        "from": dby_date_str,
        "to": y_date_str,
        "language": "en",
        "sortBy": "popularity",
        "apiKey": api_key_news
    }
    response = requests.get(url="https://newsapi.org/v2/everything", params=params)
    response.raise_for_status()
    data = response.json()["articles"]
    short_data = data[:3]
    filtered_data = [{"title": item["title"], "description": item["description"]} for item in short_data]
    return filtered_data


## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
def send_sms(percent):
    news_list = get_news()
    text = format_text(percent, news_list)

    client = Client(account_sid, auth_token)
    message = (client.messages
    .create(
        body=text,
        from_=from_number,
        to=to_number
    ))
    print(message.status)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


def format_text(percent, my_list):
    if percent > 0:
        symbol = "🔺"
        percent_text = f"{percent:.2f}%"
    else:
        symbol = "🔻"
        percent *= -1
        percent_text = f"{percent:.2f}%"

    text = f"{STOCK}: {symbol}{percent_text} \n"
    for art in my_list:
        text += f"Headline: {art["title"]} \n"
        text += f"Brief: {art["description"]} \n"
    return text


stock_price_check()
