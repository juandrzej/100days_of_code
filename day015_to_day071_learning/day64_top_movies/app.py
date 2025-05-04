from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import requests
from dotenv import load_dotenv
import os
from models import db, Movie
from forms import  AddMovieForm, RateMovieForm
from helpers import add_movie_to_db, rank_movies

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies_collection.db"
Bootstrap5(app)

# API Configuration
TMDB_ACCESS_TOKEN = os.environ['TMDB_ACCESS_TOKEN']
TMDB_URL = "https://api.themoviedb.org/3/search/movie"

# Initialize the SQLAlchemy object with the Flask app
db.init_app(app)

# Create all database tables when the app context is active (on startup)
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    """
    Home route that displays the list of movies from the database, ranked by their rating.
    Calls the rank_movies function to ensure movies are ranked properly before rendering the page.
    """
    rank_movies()
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Add movie route that allows users to search for a movie by title using TMDB API.
    If the form is submitted, the app fetches search results and passes them further to let user select exact movie.
    """
    form = AddMovieForm()
    if form.validate_on_submit():
        title = form.title.data
        headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}
        params = {"query": title}
        response = requests.get(TMDB_URL, headers=headers, params=params).json()['results']
        return render_template("select.html", movies=response)
    return render_template("add.html", form=form)


@app.route("/add_to_db")
def add_to_db():
    """
    Adds the selected movie details to the database.
    Retrieves the movie information from the query string and calls the helper function to save it.
    """
    title = request.args.get('title')
    date = request.args.get('date')
    description = request.args.get('description')
    poster = request.args.get('poster')
    movie_id = add_movie_to_db(title, date, description, poster)
    return redirect(url_for('edit', movie_id=movie_id))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    """
    Edit route that allows users to rate and review a movie.
    Displays the movie details and includes a form to input rating and review.
    """
    form = RateMovieForm()
    movie_id = request.args.get('movie_id')
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete_movie():
    """
    Delete route that removes a movie from the database.
    Retrieves the movie ID from the URL and deletes the corresponding movie record.
    """
    movie_id = request.args.get('movie_id')
    db.session.delete(db.get_or_404(Movie, movie_id))
    db.session.commit()
    return redirect(url_for('home'))


# Start the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
