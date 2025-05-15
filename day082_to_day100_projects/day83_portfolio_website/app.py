from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
import os
from dotenv import load_dotenv
import smtplib

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Load environment variables
load_dotenv()
email: str = os.environ.get("email", "")
password: str = os.environ.get("password", "")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


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
                msg=f"Subject:{data['subject']}\n\n"
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n"
                f"Message: {data['message']}",
            )
        return redirect(url_for("home"))
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
