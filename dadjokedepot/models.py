from dadjokedepot import db, loginManager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    imageFile = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    disliked = db.relationship('PostDislike', foreign_keys='PostDislike.user_id', backref='user', lazy='dynamic')
    commented = db.relationship("Comment", foreign_keys="Comment.user_id", backref="user", lazy="dynamic")

    def like_post(self, post):
        if not self.has_liked_post(post) and not self.has_disliked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def dislike_post(self, post):
        if not self.has_liked_post(post) and not self.has_disliked_post(post):
            dislike = PostDislike(user_id=self.id, post_id=post.id)
            db.session.add(dislike)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def undislike_post(self, post):
        if self.has_disliked_post(post):
            PostDislike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def has_disliked_post(self, post):
        return PostDislike.query.filter(
            PostDislike.user_id == self.id,
            PostDislike.post_id == post.id).count() > 0

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.imageFile}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jokeText = db.Column(db.Text, nullable = False)
    dateCreated = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    dislikes = db.relationship('PostDislike', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', foreign_keys="Comment.post_id", backref='post', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.id}', '{self.dateCreated}'')"

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

class PostDislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))