# Import necessary modules from Flask-SQLAlchemy and SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# Initialize the SQLAlchemy object. This will be bound to the app instance.
db = SQLAlchemy()

class Movie(db.Model):
    """
    Movie model that defines the structure of the 'movies' table in the database.
    This table will store information about each movie, such as its title, year,
    description, rating, and more.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    def __repr__(self):
        """
        String representation for the Movie object.
        Returns the movie's title to easily identify it when printed.
        """
        return f'<Movie {self.title}>'