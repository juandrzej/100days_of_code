from flask import Flask, render_template
import requests

# Initialize the Flask application
app = Flask(__name__)

# Fetch data from the API
url = 'https://api.npoint.io/05d138175271cf97b9d2'
responses = requests.get(url).json()


# Home page route
@app.route('/')
def home():
    return render_template('index.html', posts=responses)


# About page route
@app.route('/about')
def about():
    return render_template('about.html')


# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Individual post page route
@app.route('/post/<int:chosen_id>')
def post(chosen_id):
    # chosen_post =  None
    # for response in responses:
    #     if chosen_id == response['id']:
    #         chosen_post = response

    chosen_post = next((response for response in responses if response['id'] == chosen_id), None)
    return render_template('post.html', post=chosen_post)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)