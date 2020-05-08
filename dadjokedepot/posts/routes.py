from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from dadjokedepot import db
from dadjokedepot.models import Post, Comment
from dadjokedepot.posts.forms import PostForm
posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(jokeText=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Joke submitted!", "success")
        return redirect(url_for("main.home"))
    return render_template("newpost.html", title="New Post", form=form, legend="Think you're punny? Submit a Joke!")

@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash("Added comment", "success")
        return redirect(url_for("posts.view_post", post_id=post.id, form=form))
    return render_template("viewpost.html", post=post, form=form)

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.author != current_user):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.jokeText = form.content.data
        db.session.commit()
        flash("Joke updated!", "success")
        return redirect(url_for("posts.view_post", post_id=post.id))
    elif (request.method == "GET"):
        form.content.data = post.jokeText
    return render_template("newpost.html", title="Update Post", form=form, legend="Update Post")

@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.author != current_user and not current_user.isModerator):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Joke Deleted", "success")
    return redirect(url_for("main.home"))

@posts.route("/post/deletecomment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if (comment.user != current_user and not current_user.isModerator):
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted", "success")
    return redirect(request.referrer)

@posts.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@posts.route('/dislike/<int:post_id>/<action>')
@login_required
def dislike_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'dislike':
        current_user.dislike_post(post)
        db.session.commit()
    if action == 'undislike':
        current_user.undislike_post(post)
        db.session.commit()
    return redirect(request.referrer)

