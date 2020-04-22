from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dadjokedepot import db, bcrypt
from dadjokedepot.models import User, Post
from dadjokedepot.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from dadjokedepot.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if (form.validate_on_submit()):
        hashedpw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashedpw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created', 'success')
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get("next")
            if (nextPage):
                return redirect(nextPage)
            return redirect(url_for("main.home"))
        else:
            flash("Unable to login", "danger")
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.imageFile = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.imageFile)
    return render_template('accountpage.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_page(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
                      .order_by(Post.dateCreated.desc())\
                      .paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + user.imageFile)
    return render_template("userpage.html", title=username, posts=posts, user=user, image_file=image_file)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if (current_user.is_authenticated):
        return redirect(url_for("main.home"))

    form = RequestResetForm()
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Password reset email has been sent", "info")
        return redirect(url_for("users.login"))
    return render_template("requestPasswordReset.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if (current_user.is_authenticated):
        return redirect(url_for("main.home"))

    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid token. Please provide a valid email and try again.", "danger")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if (form.validate_on_submit()):
        hashedpw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashedpw
        db.session.commit()
        flash(f'Password reset successful', 'success')
        return redirect(url_for("users.login"))
        
    return render_template("resetPassword.html", title="Reset Password", form=form)