from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Decorator to make text bold
def make_bold(function):
    def wrapper():
        text = function()
        return f'<b>{text}</b>'
    return wrapper

# Home route
@app.route('/')
def hello_world():
    return ('<h1 style="text-align: center">Hello, World!</h1>'
            '<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTNoMGlkZHpvbDR3eGNkYm9vd3lrNGRtYXFkNmVlYWhqa3FpYm8xZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tHIRLHtNwxpjIFqPdV/giphy.webp" alt="Hello World GIF">')

# Route with decorator for bold text
@app.route('/bye')
@make_bold
def say_bye():
    return 'Bye'

# Dynamic route with variable paths and type conversion
@app.route('/<name>/<int:number>')
def greet(name, number):
    return f'Hello there {name}, you are {number} years old!'

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
