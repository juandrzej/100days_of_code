from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length
from flask_bootstrap import Bootstrap5


# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "secret string"  # Secret key for CSRF protection

# Initialize Flask-Bootstrap
bootstrap = Bootstrap5(app)

# Define the login form
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[Email()])
    password = PasswordField(label='Password', validators=[Length(min=8)])
    submit = SubmitField(label='Log In')

# Home route
@app.route("/")
def home():
    return render_template('index.html')

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if the login credentials are correct
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=form)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
