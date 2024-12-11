from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')

# Initialize extensions
ckeditor = CKEditor(app)
Bootstrap5(app)

# Database Model
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///posts.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Configure Table
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()



# Flask-WTF Form
class PostForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Blog Post Subtitle', validators=[DataRequired()])
    author = StringField('Blog Post Author', validators=[DataRequired()])
    img_url = StringField('URL for Background Image', validators=[DataRequired(), URL()])
    body = CKEditorField('Blog Post Body', validators=[DataRequired()])
    submit = SubmitField('Add Blog Post')


# Routes
@app.route('/')
def get_all_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)

@app.route('/new-post', methods=["GET","POST"])
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date = date.today().strftime("%B %d, %Y"),
            body = form.body.data,
            author = form.author.data,
            img_url = form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)

@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))
    return render_template("make-post.html", form=form, is_edit=True)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
