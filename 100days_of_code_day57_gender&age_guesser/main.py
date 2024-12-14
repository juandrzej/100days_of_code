from flask import Flask, render_template
import random
import datetime
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
PAGE_AUTHOR = os.getenv('PAGE_AUTHOR')

# Configuration for random number range
RANDOM_NUMBER_MIN = 1
RANDOM_NUMBER_MAX = 10


@app.route('/')
def home():
    random_number = random.randint(RANDOM_NUMBER_MIN, RANDOM_NUMBER_MAX)
    current_year = datetime.datetime.now().year
    return render_template('index.html', num=random_number, year=current_year, name=PAGE_AUTHOR)


@app.route('/guess/<name>')
def guessed_name(name):
    gender_url = f"https://api.genderize.io?name={name}"
    try:
        gender_response = requests.get(gender_url)
        gender_response.raise_for_status()
        gender_data = gender_response.json()
        gender = gender_data.get('gender', 'Unknown')
    except (requests.RequestException, ValueError):
        gender = 'Unknown'

    age_url = f"https://api.agify.io?name={name}"
    try:
        age_response = requests.get(age_url)
        age_response.raise_for_status()
        age_data = age_response.json()
        age = age_data.get('age', 'Unknown')
    except (requests.RequestException, ValueError):
        age = 'Unknown'

    return render_template('guess.html', name=name, gender=gender, age=age)


@app.route('/blog/<num>')
def blog(num):
    print(num)
    blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    try:
        response = requests.get(blog_url)
        response.raise_for_status()
        posts = response.json()
    except (requests.RequestException, ValueError):
        posts = []
    return render_template('blog.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)