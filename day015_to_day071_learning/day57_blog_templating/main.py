from flask import Flask, render_template
import requests
from post import Post

# Fetch blog data from the API
blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
posts = requests.get(blog_url).json()

# Create a list of Post objects
# post_objects = []
# for post in posts:
#     post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
#     post_objects.append(post_obj)
post_objects = [Post(post["id"], post["title"], post["subtitle"], post["body"]) for post in posts]


# Initialize Flask application
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", posts=post_objects)


@app.route('/post/<int:blog_id>')
def post(blog_id):
    # requested_post = None
    # for blog_post in post_objects:
    #     if blog_post.id == blog_id:
    #         requested_post = blog_post
    requested_post = next((blog_post for blog_post in post_objects if blog_post.id == blog_id), None)
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
