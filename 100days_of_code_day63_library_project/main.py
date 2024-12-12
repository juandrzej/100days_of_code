from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


# create the app
app = Flask(__name__)

# create database
class Base(DeclarativeBase):
  pass

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///all_books.db"

# Create the extension
db = SQLAlchemy(model_class=Base)

# initialize the app with the extension
db.init_app(app)

# create a table
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        new_book = Book(
            title=data['title'],
            author=data['author'],
            rating=int(data['rating'])
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        book_id = request.form['book_id']
        book_to_update = db.get_or_404(Book, book_id)
        rating = request.form['rating']
        book_to_update.rating = rating
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('book_id')
    book = db.get_or_404(Book, book_id)
    return render_template('change_rating.html', book=book)


@app.route("/delete")
def delete():
    book_id = request.args.get('book_id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

