import os
import csv

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField ,SubmitField
from wtforms.validators import DataRequired, URL
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)


# Define the form for adding cafes
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location on Google Maps (URL)', validators=[URL()])
    open_time = StringField('Opening Time (e.g. 8AM)', validators=[DataRequired()])
    close_time = StringField('Closing Time (e.g. 5:30AM)', validators=[DataRequired()])
    coffee_rate = SelectField('Coffee Rating', choices=['☕️'* i if i > 0 else '✘' for i in range(6)])
    wifi_rate = SelectField('Wifi Strength Rating', choices=['💪'* i if i > 0 else '✘' for i in range(6)])
    socket_rate = SelectField('Power Socket Availability', choices=['✘'] + ['🔌' * i for i in range(1, 6)])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        data = (f"\n{form.cafe.data},{form.cafe_location.data},{form.open_time.data},{form.close_time.data},"
              f"{form.coffee_rate.data},{form.wifi_rate.data},{form.socket_rate.data}")
        with open('cafe-data.csv', mode='a', encoding='utf-8') as f:
            f.write(data)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        # list_of_rows = list(csv_data)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
