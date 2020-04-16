from flask import Flask, render_template, redirect, flash, url_for, request
from dadjokedepot import app, bcrypt, db
from dadjokedepot.forms import RegistrationForm, LoginForm
from dadjokedepot.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = []

@app.route("/")
def home():
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

@app.route("/post/new")
@login_required
def new_post():
    return render_template("newpost.html", title="New Post")