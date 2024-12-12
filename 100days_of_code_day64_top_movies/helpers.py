# db is used to interact with the database, and Movie is the model representing the movies table.
from models import db, Movie

def add_movie_to_db(title, year, description, poster):
    """
    Adds a new movie to the database.
    Takes in movie title, year, description, and poster URL to create a new movie entry.
    Returns the ID of the newly added movie.
    """
    try:
        new_movie = Movie(
            title=title,
            year=int(year),
            description=description,
            rating=None,
            ranking=None,
            review=None,
            img_url=f"https://image.tmdb.org/t/p/w500{poster}"
        )

        db.session.add(new_movie)
        db.session.commit()

        return new_movie.id

    except Exception as e:
        # If an error occurs, rollback the session to undo the changes and print the error to help with debugging.
        db.session.rollback()
        print(e)

def rank_movies():
    """
    Ranks all movies in the database based on their rating.
    Retrieves all movies from the database, orders them by rating in descending order,
    and assigns a ranking to each movie based on its position in the list.
    The ranking starts from 1 (highest rating).
    Commits the ranking changes to the database.
    """
    # Fetch all movies from the database, sorted by rating in descending order
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars().all()

    # Iterate over the sorted list of movies and assign a ranking
    for index, movie in enumerate(all_movies, start=1):
        movie.ranking = index
        db.session.commit()