# Import necessary modules from Flask-WTF and WTForms.
# Flask-WTF integrates Flask with WTForms for creating and handling web forms.
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# AddMovieForm is used to create a form for adding a new movie.
class AddMovieForm(FlaskForm):
    """
    Form for adding a new movie.
    The user will provide the movie title, and submit the form to add it to the database.
    """
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

# RateMovieForm is used to rate and review an existing movie.
class RateMovieForm(FlaskForm):
    """
    Form for rating and reviewing an existing movie.
    The user will provide a rating out of 10 and a review, and submit the form to save their input.
    """
    rating = StringField('Your Rating Out of 10 (e.g. 7.5)', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Rate Movie')
