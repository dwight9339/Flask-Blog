from flask import Flask, render_template, redirect, flash, url_for
from dadjokedepot import app
from dadjokedepot.forms import RegistrationForm, LoginForm
from dadjokedepot.models import User, Post

posts = []

@app.route("/")
def home():
    return render_template("home.html", posts=posts, title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About Me")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if (form.validate_on_submit()):
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if (form.validate_on_submit()):
        flash("Successful login", 'success')
        return redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form)

