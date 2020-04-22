from flask import render_template, request, Blueprint
from dadjokedepot.models import Post, PostLike, PostDislike, Comment
from dadjokedepot import db
from sqlalchemy.sql.functions import func

main = Blueprint("main", __name__)

@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.dateCreated.desc()).paginate(per_page=5)
    return render_template("home.html", posts=posts)

@main.route("/oldest")
def oldest():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.dateCreated.asc()).paginate(per_page=5)
    return render_template("home.html", posts=posts)

@main.route("/mostpopular")
def mostpopular():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.join(PostLike).group_by(Post.id).order_by(func.count().desc()).paginate(per_page=5)
    return render_template("home.html", posts=posts)
    
@main.route("/mosthated")
def mosthated():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.join(PostDislike).group_by(Post.id).order_by(func.count().desc()).paginate(per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")