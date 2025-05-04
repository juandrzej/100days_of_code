from flask import Flask
import random

# Initiating the Flask app
app = Flask(__name__)

# Defining the range for the number to guess
MIN_NUMBER = 0
MAX_NUMBER = 9

# Generating a random number for the game
target_number = random.randint(MIN_NUMBER, MAX_NUMBER)

# Home screen route
@app.route("/")
def home():
    return ("<h1>Guess a number between 0 and 9</h1>"
            "<img src='https://i.giphy.com/tHIRLHtNwxpjIFqPdV.webp'>")

# Route to check the user's guess
@app.route("/<int:user_number>")
def check_number(user_number):
    if user_number < target_number:
        return ("<h1 style='color: red'>Too low, try again!</h1>"
                "<img src='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG1xNHRrcmVpeGhpeGhqa3I4ZjdlMTVrcmk5Mml5N2V2OXFoN2MzMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriO04qxVReM5rJEA/giphy.webp'>")
    elif user_number > target_number:
        return ("<h1 style='color: red'>Too high, try again!</h1>"
                "<img src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmlwaHF3YmZ2YXh6MngxOGFxdDBqd2p4dzFwOHE2NnJhNXcwdXFnZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/7J4Lvpz55rocVYccdH/giphy.webp'>")
    else:
        return ("<h1 style='color: purple'>You found me!</h1>"
                "<img src='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmp0Zm14ZWxyMWoza3RlZDBndGQ1cGY1NGxlcnYydXNxMGp0dWYzdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/I8nepxWwlEuqI/200w.webp'>")

# Running the app
if __name__ == "__main__":
    app.run(debug=True)
