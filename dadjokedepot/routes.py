from flask import Flask, render_template, redirect, flash, url_for, request, abort
from dadjokedepot import app, bcrypt, db
from dadjokedepot.forms import RegistrationForm, LoginForm, PostForm
from dadjokedepot.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.dateCreated.desc()).paginate(per_page=5)
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()
    if (form.validate_on_submit()):
        hashedpw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashedpw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created', 'success')
        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get("next")
            if (nextPage):
                return redirect(nextPage)
            return redirect(url_for("home"))
        else:
            flash("Unable to login", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account")
@login_required
def account():
    return render_template("accountpage.html", title="Account")

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(jokeText=form.joke.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Joke submitted!", "success")
        return redirect(url_for("home"))
    return render_template("newpost.html", title="New Post", form=form, legend="Think you're punny? Submit a Joke!")

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("viewpost.html", post=post)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.author != current_user):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.jokeText = form.joke.data
        db.session.commit()
        flash("Joke updated!", "success")
        return redirect(url_for("view_post", post_id=post.id))
    elif (request.method == "GET"):
        form.joke.data = post.jokeText
    return render_template("newpost.html", title="Update Post", form=form, legend="Update Post")

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.author != current_user):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Joke Deleted", "success")
    return redirect(url_for("home"))

@app.route("/user/<string:username>")
def user_page(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
                      .order_by(Post.dateCreated.desc())\
                      .paginate(page=page, per_page=5)
    return render_template("userpage.html", title=username, posts=posts, user=user)