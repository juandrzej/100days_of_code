import os
from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv

# Fetch posts data from an external API
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables
load_dotenv()
email = os.environ.get("email")
password = os.environ.get("password")


# Home page route
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)

# About page route
@app.route("/about")
def about():
    return render_template("about.html")

# Contact page route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form

        # Send contact data via email
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs=email,
                msg=f"Subject:New Contact Form Submission\n\nName: {data['name']}\nEmail: {data['email']}\nMessage: {data['message']}"
            )

    return render_template("contact.html")

# Specific blog post route
@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    # requested_post = next((post for post in posts if post["id"] == index), None)
    return render_template("post.html", post=requested_post)

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=5001)
