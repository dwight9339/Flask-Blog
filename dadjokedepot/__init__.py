import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dadjokedepot.config import Config
from flask_migrate import Migrate

# Create app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize services
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = "users.login"
loginManager.login_message_category = "info"
mail = Mail(app)
migrate = Migrate(app, db)

# Import blueprints
from dadjokedepot.users.routes import users
from dadjokedepot.posts.routes import posts
from dadjokedepot.main.routes import main
from dadjokedepot.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)


# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)

#     db.init_app(app)
#     bcrypt.init_app(app)
#     loginManager.init_app(app)
#     mail.init_app(app)
    
#     from dadjokedepot.users.routes import users
#     from dadjokedepot.posts.routes import posts
#     from dadjokedepot.main.routes import main
#     from dadjokedepot.errors.handlers import errors
#     app.register_blueprint(users)
#     app.register_blueprint(posts)
#     app.register_blueprint(main)
#     app.register_blueprint(errors)


#     return app