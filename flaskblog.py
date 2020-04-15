from flask import Flask, render_template, redirect, flash, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '36384a4439d0abf7437362c0130106a7'

posts = [
    {
        "author": "Heidi Helmsworth",
        "title": "Blog Post 1",
        "content": "My first post......",
        "date_posted": "April 12, 2018"
    }
]

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

if __name__ == "__main__":
    app.run(debug=True)