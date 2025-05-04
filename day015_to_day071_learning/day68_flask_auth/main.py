from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if unauthorized

# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# User model
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]

        # Check if the user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please log in.")
            return redirect(url_for("login"))

        # Hash password and create a new user
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_user = User(email=email, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        login_user(new_user)
        return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Find user by email
        user = db.session.execute(db.select(User).where(User.email==email)).scalar_one_or_none()

        # Check email
        if not user:
            flash('The email does not exist, please try again.')
            return redirect(url_for('login'))

        # Check password
        if not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))

        # Log in the user
        login_user(user)
        return redirect(url_for("secrets"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name, logged_in=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory("static","files/cheat_sheet.pdf")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
