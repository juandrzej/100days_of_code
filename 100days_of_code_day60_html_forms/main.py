from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Login route to handle form submission
@app.route('/login', methods=['POST'])
def receive_data():
    username = request.form['username']
    password = request.form['password']
    return f'<h1>Name: {username}, Password: {password}</h1>'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
